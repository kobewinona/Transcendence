const script = document.createElement("script");
script.type = "text/javascript";


function register(fn, call=false, name=null) {
	if (!script.innerHTML.includes(`function ${fn.name}`)) {
		script.innerHTML += fn.toString() + "\n";
		if (call) {
			script.innerHTML += `${fn.name}();\n`;
		}
	}
}

export {register, script};
