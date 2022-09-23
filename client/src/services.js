const services = {
    fetch_post: async function (url, bodyObj) {
        const r = await fetch("/api/" + url, {
            method: 'post',
            body: JSON.stringify(bodyObj),
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const data = await r.json();
        return data;
    },
    fetch_auth: async function (url, bodyObj = null) {
        const r = await fetch("/api/" + url, {
            method: 'get',
            body: bodyObj ? JSON.stringify(bodyObj) : null,
            headers: {
                'Content-Type': 'application/json',
                "Authorization": "Bearer " + localStorage.getItem('token')
            },
        });
        const data = await r.json();
        return data;
    }
}
export default services;