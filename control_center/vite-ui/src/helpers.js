
export function resolveHost() {
	let host = window.location.host
	if (process.env.SERVER_HOST == null) {
		host = host.replace(/:.*$/,  `:${process.env.SERVER_PORT}`)
	} else {
		host = `http://${process.env.SERVER_HOST}:${process.env.SERVER_PORT}`
	}
	return host
}


export function get(path, promise, errorPromise) {
  const host = resolveHost()
  fetch(`http://${host}/${path}`, {
    method: "get",
    mode: 'cors'
  })
  .then((response) => response.json())
  .then(promise )
  .catch(errorPromise)
}

export function request(path, method, payload, promise, errorPromise) {
  const host = resolveHost()
  fetch(`http://${host}/${path}`, {
    method: method,
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
    mode: 'cors'
  })
  .then((response) => response.json())
  .then(promise)
  .catch(errorPromise)
}