async function parseCSV() {
  const fileInput = document.getElementById('csvFileInput')
  const output = document.getElementById('output')

  if (!fileInput.files.length) {
    output.value = 'Please select a CSV file first.'
    return
  }

  const filePath = fileInput.files[0].path
  output.value = 'Processing...\n'

  try {
    const result = await window.api.parseCSV(filePath)
    output.value = result
  } catch (error) {
    output.value = `Error: ${error}`
  }
}
