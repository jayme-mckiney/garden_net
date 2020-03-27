
function resolveHost() {
	let host = window.location.host
	let debug = false
	console.log(process.env)
	if (debug) {
		host = host.replace(/:.*$/,  "5000")
	}
	return host
}


export default resolveHost;