
function resolveHost() {
	let host = window.location.host
	if (process.env && process.env.NODE_ENV === "development") {
		host = host.replace(/:.*$/,  ":5000")
	}
	return host
}


export default resolveHost;