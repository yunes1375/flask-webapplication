import { Material } from 'three';
import { IFCModel } from 'web-ifc-three/IFC/components/IFCModel';
import { IfcManager } from '../ifc';
import { IfcContext } from '../context';
export declare class SectionFillManager {
    private IFC;
    private context;
    readonly fills: {
        [name: string]: IFCModel;
    };
    constructor(IFC: IfcManager, context: IfcContext);
    create(name: string, modelID: number, ids: number[], material: Material): IFCModel | null;
    delete(name: string): void;
    private setupMaterial;
    private getSubset;
}
