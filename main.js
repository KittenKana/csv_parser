const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { execFile } = require('child_process')

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  win.loadFile('renderer/index.html')
}

ipcMain.handle('parse-csv', async (_, filePath) => {
  return new Promise((resolve, reject) => {
    execFile('python', ['parser/parser.py', filePath], (error, stdout, stderr) => {
      if (error) {
        reject(stderr)
      } else {
        resolve(stdout)
      }
    })
  })
})

app.whenReady().then(() => {
  createWindow()
})
