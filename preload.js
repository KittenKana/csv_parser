const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  parseCSV: (filePath) => ipcRenderer.invoke('parse-csv', filePath)
})
