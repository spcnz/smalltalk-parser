import * as net from 'net';
import { workspace, ExtensionContext, Disposable } from 'vscode';
import {
	LanguageClient,
	LanguageClientOptions,
	StreamInfo,
} from 'vscode-languageclient/node';

let client: LanguageClient;

function startLangServerTCP(addr: number): Disposable {

	let serverOptions = () => {
        // Connect to language server via socket
        let socket = net.connect(addr, "localhost");
        let result: StreamInfo = {
            writer: socket,
            reader: socket
        };
        return Promise.resolve(result);
    };

	const clientOptions: LanguageClientOptions = {
			documentSelector: [{ scheme: 'file', language: 'plaintext' }],
			synchronize: {
				// Notify the server about file changes to '.clientrc files contained in the workspace
				fileEvents: workspace.createFileSystemWatcher('**/.st')
			}
	}
	return new LanguageClient(`tcp lang server (port ${addr})`, serverOptions, clientOptions).start();
}

export function activate(context: ExtensionContext) {
	let lsDisp: Disposable = null;
	lsDisp = startLangServerTCP(8013);
	context.subscriptions.push(lsDisp);
}
export function deactivate(): Thenable<void> | undefined {
	if (!client) {
		return undefined;
	}
	return client.stop();
}