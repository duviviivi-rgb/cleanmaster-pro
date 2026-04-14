import { defineStore } from 'pinia'

export interface Material {
  id: string
  name: string
  model: string
  quantity: number
  unit: string
  position: string
  floor: string
  drawing_number: string
  drawing_name: string
  category: string
  inspection_batch: string
  standard: string
}

export const useMaterialStore = defineStore('material', {
  state: () => ({
    materials: [] as Material[],
    isExtracting: false,
    currentMaterial: null as Material | null
  }),
  actions: {
    addMaterial(material: Material) {
      this.materials.push(material)
    },
    addMaterials(materials: Material[]) {
      this.materials = [...this.materials, ...materials]
    },
    updateMaterial(id: string, updates: Partial<Material>) {
      const index = this.materials.findIndex(m => m.id === id)
      if (index !== -1) {
        this.materials[index] = { ...this.materials[index], ...updates }
      }
    },
    removeMaterial(id: string) {
      this.materials = this.materials.filter(m => m.id !== id)
    },
    clearMaterials() {
      this.materials = []
    },
    setCurrentMaterial(material: Material | null) {
      this.currentMaterial = material
    },
    setIsExtracting(extracting: boolean) {
      this.isExtracting = extracting
    },
    getMaterialsByFloor(floor: string) {
      return this.materials.filter(m => m.floor === floor)
    },
    getMaterialsByDrawing(drawingNumber: string) {
      return this.materials.filter(m => m.drawing_number === drawingNumber)
    }
  }
})
