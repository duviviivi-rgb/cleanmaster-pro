import { defineStore } from 'pinia'

export interface FileItem {
  id: string
  name: string
  path: string
  type: string
  size: number
  status: 'pending' | 'processing' | 'success' | 'error'
  progress: number
}

export const useFileStore = defineStore('file', {
  state: () => ({
    files: [] as FileItem[],
    isUploading: false,
    currentFile: null as FileItem | null
  }),
  actions: {
    addFile(file: FileItem) {
      this.files.push(file)
    },
    updateFileStatus(id: string, status: FileItem['status']) {
      const file = this.files.find(f => f.id === id)
      if (file) {
        file.status = status
      }
    },
    updateFileProgress(id: string, progress: number) {
      const file = this.files.find(f => f.id === id)
      if (file) {
        file.progress = progress
      }
    },
    removeFile(id: string) {
      this.files = this.files.filter(f => f.id !== id)
    },
    clearFiles() {
      this.files = []
    },
    setCurrentFile(file: FileItem | null) {
      this.currentFile = file
    },
    setIsUploading(uploading: boolean) {
      this.isUploading = uploading
    }
  }
})
