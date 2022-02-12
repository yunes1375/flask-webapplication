import { GridHelper } from 'three';
import { IfcComponent } from '../../base-types';
export class IfcGrid extends IfcComponent {
    constructor(context) {
        super(context);
        this.context = context;
    }
    setGrid(size, divisions, colorCenterLine, colorGrid) {
        if (this.grid) {
            if (this.grid.parent)
                this.grid.removeFromParent();
            this.grid.geometry.dispose();
        }
        this.grid = new GridHelper(size, divisions, colorCenterLine, colorGrid);
        this.grid.renderOrder = 0;
        const scene = this.context.getScene();
        scene.add(this.grid);
    }
}
//# sourceMappingURL=grid.js.map