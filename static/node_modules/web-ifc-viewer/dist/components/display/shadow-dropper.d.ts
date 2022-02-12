import { Camera, Group, Mesh, WebGLRenderTarget } from 'three';
import { IfcManager } from '../ifc';
import { IfcContext } from '../context';
export interface Shadow {
    root: Group;
    rt: WebGLRenderTarget;
    rtBlur: WebGLRenderTarget;
    blurPlane: Mesh;
    camera: Camera;
}
export declare class ShadowDropper {
    shadows: {
        [modelID: number]: Shadow;
    };
    cameraHeight: number;
    darkness: number;
    opacity: number;
    resolution: number;
    amount: number;
    planeColor: number;
    private tempMaterial;
    private depthMaterial;
    private context;
    private IFC;
    constructor(context: IfcContext, IFC: IfcManager);
    renderShadow(modelID: number): Promise<void>;
    private createPlanes;
    private initializeShadow;
    private bakeShadow;
    private initializeCamera;
    private initializeRenderTargets;
    private initializeRoot;
    private createGroundColorPlane;
    private createBasePlane;
    private createBlurPlane;
    private createPlaneMaterial;
    private initializeDepthMaterial;
    private createShadow;
    private createCamera;
    private getSizeAndCenter;
    private getLowestYCoordinate;
    private blurShadow;
}
