/**
 * VRMode - WebXR immersive visualization for Magen-Live
 *
 * Renders the Deck.gl/MapLibre map canvas as a texture inside a Three.js
 * WebXR scene. Users see the live map on a curved screen in VR with
 * hand-tracking interaction for zoom and rotation.
 *
 * Architecture:
 * - MapLibre/Deck.gl continues rendering to its own canvas (unchanged)
 * - Three.js captures that canvas as a CanvasTexture each frame
 * - The texture is mapped onto a curved CylinderGeometry in the VR scene
 * - Data overlays (flights, satellites) could later be rendered as
 *   native Three.js objects for true 3D depth
 */
import * as THREE from 'three';
import { VRButton } from 'three/addons/webxr/VRButton.js';
import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';

export interface VRModeOptions {
  /** The MapLibre/Deck.gl canvas element to mirror */
  mapCanvas: HTMLCanvasElement;
  /** Container element (for inserting the VR button) */
  container: HTMLElement;
  /** Callback when VR session starts (pause map interactions) */
  onVRStart?: () => void;
  /** Callback when VR session ends (resume map interactions) */
  onVREnd?: () => void;
}

export class VRMode {
  private renderer: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private cameraRig: THREE.Group;
  private mapTexture: THREE.CanvasTexture;
  private mapScreen: THREE.Mesh;
  private mapCanvas: HTMLCanvasElement;
  private vrButton: HTMLElement | null = null;
  private isActive = false;
  private controllers: THREE.Group[] = [];
  private controllerGrips: THREE.Group[] = [];
  private raycaster = new THREE.Raycaster();
  private onVRStart?: () => void;
  private onVREnd?: () => void;

  // Interaction state
  private isDragging = false;
  private dragController: THREE.Group | null = null;
  private previousControllerPos = new THREE.Vector3();
  private mapRotation = 0;

  // Reusable vectors (avoid GC pressure in render loop)
  private readonly _tempVec = new THREE.Vector3();
  private readonly _tempVec2 = new THREE.Vector3();

  constructor(options: VRModeOptions) {
    this.mapCanvas = options.mapCanvas;
    this.onVRStart = options.onVRStart;
    this.onVREnd = options.onVREnd;

    // Create Three.js renderer (shares the page, hidden until VR starts)
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.xr.enabled = true;
    this.renderer.xr.setFoveation(1.0);
    this.renderer.xr.setReferenceSpaceType('local-floor');

    // Hide the Three.js canvas (VR renders to headset, not screen)
    this.renderer.domElement.style.display = 'none';
    document.body.appendChild(this.renderer.domElement);

    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x050510);

    // Ambient starfield effect
    this.addStarfield();

    // Lighting
    const ambient = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambient);
    const directional = new THREE.DirectionalLight(0xffffff, 0.4);
    directional.position.set(5, 10, 5);
    this.scene.add(directional);

    // Camera rig (headset controls camera, rig controls world position)
    this.camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 100);
    this.cameraRig = new THREE.Group();
    this.cameraRig.add(this.camera);
    this.scene.add(this.cameraRig);

    // Map texture from the Deck.gl/MapLibre canvas
    this.mapTexture = new THREE.CanvasTexture(this.mapCanvas);
    this.mapTexture.minFilter = THREE.LinearFilter;
    this.mapTexture.magFilter = THREE.LinearFilter;
    this.mapTexture.colorSpace = THREE.SRGBColorSpace;

    // Curved screen to display the map (180-degree cylinder segment)
    this.mapScreen = this.createMapScreen();
    this.scene.add(this.mapScreen);

    // Add a subtle floor grid for spatial reference
    this.addFloorGrid();

    // Controllers
    this.setupControllers();

    // VR session events
    this.renderer.xr.addEventListener('sessionstart', () => {
      this.isActive = true;
      this.onVRStart?.();
    });
    this.renderer.xr.addEventListener('sessionend', () => {
      this.isActive = false;
      this.onVREnd?.();
    });

    // Start the render loop
    this.renderer.setAnimationLoop(this.onFrame.bind(this));
  }

  /**
   * Create a curved screen mesh for displaying the map.
   * Uses a cylinder segment (180 degrees) positioned around the user.
   */
  private createMapScreen(): THREE.Mesh {
    const radius = 4;
    const height = 2.5;
    const segments = 64;
    const thetaStart = Math.PI * 0.25; // start 45 degrees from front
    const thetaLength = Math.PI * 1.5; // 270-degree wrap

    // CylinderGeometry with open ends, only the inner surface visible
    const geometry = new THREE.CylinderGeometry(
      radius, radius, height, segments, 1, true,
      thetaStart, thetaLength
    );

    const material = new THREE.MeshBasicMaterial({
      map: this.mapTexture,
      side: THREE.BackSide, // render inner surface
      toneMapped: false,
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 1.5, 0); // eye level
    mesh.name = 'map-screen';

    return mesh;
  }

  /** Simple starfield background for spatial context */
  private addStarfield(): void {
    const starCount = 2000;
    const positions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      const r = 40 + Math.random() * 40;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({
      color: 0xaaaacc,
      size: 0.15,
      sizeAttenuation: true,
    });
    const stars = new THREE.Points(geometry, material);
    stars.name = 'starfield';
    this.scene.add(stars);
  }

  /** Floor reference grid */
  private addFloorGrid(): void {
    const grid = new THREE.GridHelper(20, 20, 0x222244, 0x111122);
    grid.position.y = 0;
    grid.name = 'floor-grid';
    this.scene.add(grid);
  }

  /** Set up VR controllers with ray visualization */
  private setupControllers(): void {
    const controllerModelFactory = new XRControllerModelFactory();

    for (let i = 0; i < 2; i++) {
      // Controller target ray (for pointing/raycasting)
      const controller = this.renderer.xr.getController(i);
      controller.addEventListener('selectstart', () => this.onSelectStart(controller));
      controller.addEventListener('selectend', () => this.onSelectEnd(controller));
      this.scene.add(controller);
      this.controllers.push(controller);

      // Visual ray line
      const rayGeometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0, -4),
      ]);
      const rayMaterial = new THREE.LineBasicMaterial({
        color: 0x00ccff,
        transparent: true,
        opacity: 0.6,
      });
      controller.add(new THREE.Line(rayGeometry, rayMaterial));

      // Controller grip model
      const grip = this.renderer.xr.getControllerGrip(i);
      grip.add(controllerModelFactory.createControllerModel(grip));
      this.scene.add(grip);
      this.controllerGrips.push(grip);
    }
  }

  /** Handle controller trigger press (start drag to rotate map) */
  private onSelectStart(controller: THREE.Group): void {
    // Check if pointing at the map screen
    controller.getWorldPosition(this._tempVec);
    controller.getWorldDirection(this._tempVec2).negate();

    this.raycaster.set(this._tempVec, this._tempVec2);
    const intersects = this.raycaster.intersectObject(this.mapScreen);

    if (intersects.length > 0) {
      this.isDragging = true;
      this.dragController = controller;
      controller.getWorldPosition(this.previousControllerPos);
    }
  }

  /** Handle controller trigger release */
  private onSelectEnd(_controller: THREE.Group): void {
    this.isDragging = false;
    this.dragController = null;
  }

  /** Main render loop (called by Three.js setAnimationLoop) */
  private onFrame(_timestamp: number, _frame?: XRFrame): void {
    if (!this.isActive && !this.renderer.xr.isPresenting) {
      // Not in VR, minimal update
      return;
    }

    // Update the map texture from the live canvas
    this.mapTexture.needsUpdate = true;

    // Handle drag interaction (rotate the map screen)
    if (this.isDragging && this.dragController) {
      this.dragController.getWorldPosition(this._tempVec);
      const dx = this._tempVec.x - this.previousControllerPos.x;
      this.mapRotation += dx * 0.5;
      this.mapScreen.rotation.y = this.mapRotation;
      this.previousControllerPos.copy(this._tempVec);
    }

    // Render
    this.renderer.render(this.scene, this.camera);
  }

  /** Create and attach the "Enter VR" button to the UI */
  public createVRButton(): HTMLElement {
    // Check WebXR support
    if (!('xr' in navigator)) {
      const btn = document.createElement('button');
      btn.textContent = 'VR Not Supported';
      btn.className = 'vr-button vr-not-supported';
      btn.disabled = true;
      return btn;
    }

    this.vrButton = VRButton.createButton(this.renderer);
    this.vrButton.classList.add('magen-vr-button');

    return this.vrButton;
  }

  /** Check if WebXR VR is supported in this browser */
  public static async isSupported(): Promise<boolean> {
    if (!('xr' in navigator)) return false;
    try {
      return await navigator.xr!.isSessionSupported('immersive-vr');
    } catch {
      return false;
    }
  }

  /** Clean up all resources */
  public destroy(): void {
    this.renderer.setAnimationLoop(null);
    this.renderer.xr.enabled = false;

    // Remove DOM elements
    this.renderer.domElement.remove();
    this.vrButton?.remove();

    // Dispose Three.js resources
    this.mapTexture.dispose();
    this.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        obj.geometry.dispose();
        if (Array.isArray(obj.material)) {
          obj.material.forEach((m) => m.dispose());
        } else {
          obj.material.dispose();
        }
      }
    });
    this.renderer.dispose();
  }
}
