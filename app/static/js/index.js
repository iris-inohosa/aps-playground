const options = {
    env: "AutodeskProduction",
    language: "de",
    getAccessToken: function (onSuccess) {
        fetch('/auth/2leggedtoken/').then(resp => {
            if (resp.ok) {
                resp.json().then(data => {
                    // console.log(data);
                    const { accessToken, expire } = data;
                    onSuccess(accessToken, expire);
                })
            }
            else {
                throw new Error(resp.text());
            }
        })

    }
};

// callback function, than will be called after initialization in finished
let initViewer = new Promise(function (resolve, reject) {
    Autodesk.Viewing.Initializer(options, function () {
        const container = document.getElementById('model-viewer');
        const viewer = new Autodesk.Viewing.GuiViewer3D(container);
        const viewerCode = viewer.start();

        if (viewerCode != 0) {
            reject(viewerCode)
        }
        else {
            resolve(viewer);
        }
    });
})

initViewer.then(viewer => {
    // console.log(viewer);
    // Load model
    const documentId = 'urn:' + 'dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6c2FtcGxlLXByb2plY3RzL0RBQ0hfc2FtcGxlX3Byb2plY3QucnZ0'
    Autodesk.Viewing.Document.load(
        documentId,
        function onModelLoadSucceed(doc) {
            viewer.loadDocumentNode(doc, doc.getRoot().getDefaultGeometry());
        },
        function onModelLoadFailed(errCode, errMsg) {
            console.error('Failed to load manifest [' + errCode + '] ' + errMsg);
        }
    )

}).catch(reject => {

    console.error('Initalization failed:', reject);
})




