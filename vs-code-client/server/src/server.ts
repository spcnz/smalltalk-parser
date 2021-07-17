/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
import {
	createConnection,
	TextDocuments,
	ProposedFeatures,
	InitializeParams,
	DidChangeConfigurationNotification,
	CompletionItem,
	CompletionItemKind,
	TextDocumentPositionParams,
	TextDocumentSyncKind,
	InitializeResult,
	Location,
	TextDocumentIdentifier,
	ReferenceParams,
	TextDocumentContentChangeEvent,
	TextDocumentChangeEvent
} from 'vscode-languageserver/node';

const axios = require('axios');
import * as debounce from "debounce";

import {
	TextDocument
} from 'vscode-languageserver-textdocument';

// Create a connection for the server, using Node's IPC as a transport.
// Also include all preview / proposed LSP features.
const connection = createConnection(ProposedFeatures.all);

// Create a simple text document manager.
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

let hasConfigurationCapability = false;
let hasWorkspaceFolderCapability = false;
let hasDiagnosticRelatedInformationCapability = false;

connection.onInitialize((params: InitializeParams) => {
	const capabilities = params.capabilities;

	// Does the client support the `workspace/configuration` request?
	// If not, we fall back using global settings.
	hasConfigurationCapability = !!(
		capabilities.workspace && !!capabilities.workspace.configuration
	);
	hasWorkspaceFolderCapability = !!(
		capabilities.workspace && !!capabilities.workspace.workspaceFolders
	);
	hasDiagnosticRelatedInformationCapability = !!(
		capabilities.textDocument &&
		capabilities.textDocument.publishDiagnostics &&
		capabilities.textDocument.publishDiagnostics.relatedInformation
	);

	const result: InitializeResult = {
		capabilities: {
			textDocumentSync: TextDocumentSyncKind.Incremental,
			// Tell the client that this server supports code completion.
			completionProvider: {
				resolveProvider: true
			},
			referencesProvider: {
				
			},
			workspace: {

			}
		}
	};
	if (hasWorkspaceFolderCapability) {
		result.capabilities.workspace = {
			workspaceFolders: {
				supported: true
			}
		};
	}
	return result;
});

connection.onInitialized(() => {
	parseDocuments()

	if (hasConfigurationCapability) {
		// Register for all configuration changes.
		connection.client.register(DidChangeConfigurationNotification.type, undefined);
	}
	if (hasWorkspaceFolderCapability) {
	
		connection.workspace.onDidChangeWorkspaceFolders(_event => {
			connection.console.log('Workspace folder change event received.');
		});
	}
	
});



async function parseDocuments(): Promise<void> {
	connection.console.log("Creating parser...")
	try {
		const parser =  await axios.post('http://localhost:8000/', 
		{
			method : "textDocument.DidOpen",
			params: [{
						"uri": "examples\\"
					}],
			jsonrpc: "2.0"
		})
		connection.console.log("Parser created!")
	} catch (e) {}
}

// The example settings
interface ExampleSettings {
	maxNumberOfProblems: number;
}

// The global settings, used when the `workspace/configuration` request is not supported by the client.
// Please note that this is not the case when using this server with the client provided in this example
// but could happen with other clients.
const defaultSettings: ExampleSettings = { maxNumberOfProblems: 1000 };
let globalSettings: ExampleSettings = defaultSettings;

// Cache the settings of all open documents
const documentSettings: Map<string, Thenable<ExampleSettings>> = new Map();

connection.onDidChangeConfiguration(change => {
	connection.console.log("eheh tu sam ")
	if (hasConfigurationCapability) {
		// Reset all cached document settings
		documentSettings.clear();
	} else {
		globalSettings = <ExampleSettings>(
			(change.settings.languageServerExample || defaultSettings)
		);
	}

	// Revalidate all open text documents
	documents.all().forEach(validateTextDocument);
});

function getDocumentSettings(resource: string): Thenable<ExampleSettings> {
	if (!hasConfigurationCapability) {
		return Promise.resolve(globalSettings);
	}
	let result = documentSettings.get(resource);
	if (!result) {
		result = connection.workspace.getConfiguration({
			scopeUri: resource,
			section: 'languageServerExample'
		});
		documentSettings.set(resource, result);
	}
	return result;
}

// Only keep settings for open documents
documents.onDidClose(e => {
	documentSettings.delete(e.document.uri);
});

// The content of a text document has changed. This event is emitted
// when the text document first opened or when its content has changed.
documents.onDidChangeContent(debounce((change : TextDocumentChangeEvent<TextDocument>) => {
	validateTextDocument(change.document);
}, 2000));



async function validateTextDocument(textDocument: TextDocument): Promise<void> {

	const text = textDocument.getText();
	let index = textDocument.uri.indexOf("examples")
	connection.console.log("Parsing changed doc...")
	
	try {
		const result =  await axios.post('http://localhost:8000/', 
		{
			method : "textDocument.DidChange",
			params: [{
						textDocument: { uri : textDocument.uri.slice(index).split("/").join( "\\") },
						contentChanges: { text }
					}],
			jsonrpc: "2.0"
		})
		connection.console.log("Parsed!")
	} catch (e) {}
}

connection.onDidChangeWatchedFiles(_change => {
	// Monitored files have change in VSCode
	console.log(_change)
	connection.console.log('We received an file change event');
});

// This handler provides the initial list of the completion items.
connection.onCompletion(
	(_textDocumentPosition: TextDocumentPositionParams): CompletionItem[] => {
		// The pass parameter contains the position of the text document in
		// which code complete got requested. For the example we ignore this
		// info and always provide the same completion items.
		return [
			{
				label: 'TypeScript',
				kind: CompletionItemKind.Text,
				data: 1
			},
			{
				label: 'JavaScript',
				kind: CompletionItemKind.Text,
				data: 2
			},
			{
				label: 'radi runtime izmena',
				kind: CompletionItemKind.Text,
				data: 3
			}
		];
	}
);

// This handler resolves additional information for the item selected in
// the completion list.
connection.onCompletionResolve(
	(item: CompletionItem): CompletionItem => {
		if (item.data === 1) {
			item.detail = 'TypeScript details';
			item.documentation = 'TypeScript documentation';
		} else if (item.data === 2) {
			item.detail = 'JavaScript details';
			item.documentation = 'JavaScript documentation';
		}
		return item;
	}
);

connection.onReferences(
	async (params: ReferenceParams):  Promise<Location[]> => {
		let index = params.textDocument.uri.indexOf("examples")
		params.position.line += 1
		params.position.character += 1
		params.textDocument.uri =  params.textDocument.uri.slice(index).split("/").join( "\\")

		connection.console.log("Finding references in file " + params.textDocument.uri + " on line :" +  params.position.line + " char : " + params.position.character)
		
        try {
            let resp = await axios.post('http://localhost:8000/', 
			{
				method: "textDocument.References",
				params: [params],
				jsonrpc: "2.0",
				id : 4
			}
			)

			let locs: Location[] = resp.data.result
			locs = locs.map((loc: Location) => {
				loc.uri = "file:///" + loc.uri
				loc.range.start.line -= 1
				loc.range.start.character -= 1
				loc.range.end.line -= 1
				loc.range.end.character -= 1
				return loc
			})

			return locs
		}
		catch (e) {
            return []
        }
})


type GoResponse = {
	data : {
		result: Location[];
		error: Object,
		id: string
	}
};

// Make the text document manager listen on the connection
// for open, change and close text document events
documents.listen(connection);

// Listen on the connection
connection.listen();
