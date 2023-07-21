
export function resolveHost() {
	let host = window.location.host
	if (process.env.SERVER_HOST == null) {
		host = host.replace(/:.*$/,  `:${process.env.SERVER_PORT}`)
	} else {
		host = `http://${process.env.SERVER_HOST}:${process.env.SERVER_PORT}`
	}
	return host
}

