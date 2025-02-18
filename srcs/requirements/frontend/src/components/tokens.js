// import 

export const setToken = async (token) => {
	this.$cookies.set('access_token', token.access)
	this.$cookies.set('refresh_token', token.refresh)
};

export const unsetToken = async () => {

	this.$cookies.remove('access_token')
	this.$cookies.remove('refresh_token')
}

export const getToken = async () => {
	return this.$cookies.get('access_token');
}

export const getTokenPayload = () => {
    const token = this.$cookies.get('access_token');
    if (!token) return null;

    try {
        const [, payloadBase64] = token.split('.');
        const payloadJson = atob(payloadBase64);
        const payload = JSON.parse(payloadJson);
        return payload;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
};










// // Function to set a cookie
// function setCookie(name, value, seconds) {
// 	let expires = new Date(new Date().getTime() + seconds * 1000).toUTCString();
// 	document.cookie = name + "=" + escape(value) + "; expires=" + expires + "; path=/";
// }

// // Function to get a cookie
// function getCookie(name) {
// 	let items = document.cookie.split(";");
// 	for (let i = 0; i < items.length; i++) {
// 		if (items[i].trim().startsWith(name + "=")) {
// 			return unescape(items[i].trim().substring(name.length + 1));
// 		}
// 	}
// }

// function deleteCookie(name) {
// 	document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
// }

// register(getCookie);
// register(setCookie);
// register(deleteCookie);

// export { setCookie, getCookie, deleteCookie };
