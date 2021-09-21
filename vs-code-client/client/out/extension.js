"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const net = require("net");
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
let client;
function startLangServerTCP(addr) {
    let serverOptions = () => {
        // Connect to language server via socket
        let socket = net.connect(addr, "localhost");
        let result = {
            writer: socket,
            reader: socket
        };
        return Promise.resolve(result);
    };
    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'plaintext' }],
        synchronize: {
            // Notify the server about file changes to '.clientrc files contained in the workspace
            fileEvents: vscode_1.workspace.createFileSystemWatcher('**/.st')
        }
    };
    return new node_1.LanguageClient(`tcp lang server (port ${addr})`, serverOptions, clientOptions).start();
}
function activate(context) {
    let lsDisp = null;
    lsDisp = startLangServerTCP(8013);
    context.subscriptions.push(lsDisp);
}
exports.activate = activate;
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map