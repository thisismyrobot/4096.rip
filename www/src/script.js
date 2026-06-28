/* global StlViewer */
const generator = (function () { // eslint-disable-line no-unused-vars
  const viewers = {}

  const render = function (id, path, subFolder = 'library', cameraX = -50, cameraY = 40) {
    const canvasParentElem = document.getElementById(id)
    const stlPath = `${subFolder}/${path}`
    const model = { id: 0, filename: `../${stlPath}`, color: '#00f5ff' }
    if (viewers[id]) {
      viewers[id].clean()
      viewers[id].add_model(model)
    } else {
      viewers[id] = new StlViewer(canvasParentElem, {
        allow_drag_and_drop: false,
        mouse_zoom: false,
        camerax: cameraX,
        cameray: cameraY,
        models: [model]
      })
    }
    canvasParentElem.parentElement.querySelector('a').setAttribute('href', stlPath)
    canvasParentElem.parentElement.querySelector('a').innerText = path
  }

  const generate = function (left, right) {
    render('stl-left', `${left}.stl`)
    render('stl-right', `${right}.stl`)
    render('stl-holder', 'holder.stl', 'holder', 30, 20)
  }

  return {
    generate,
    validateProfiles: profiles => profiles.length === 2 && profiles.every(profile => /^[1-4]{6}$/.test(profile))
  }
}())
