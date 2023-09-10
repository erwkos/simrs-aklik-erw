const xhr = new XMLHttpRequest();

export const DataRequest = (method, data_url, data_form) => {
    return new Promise((resolve, reject) => {
        xhr.open(method, data_url, true);
        xhr.setRequestHeader('x-requested-with', 'XMLHttpRequest');

        if (method == "post" && data_form) {
            xhr.setRequestHeader('X-CSRFToken', data_form.get('csrfmiddlewaretoken'));
            xhr.send(data_form);
        } else {
            xhr.send(null);
        };

        xhr.onload = () => {
            if (xhr.status >= 200){
                resolve(xhr);
            };

            if (xhr.status == 500){
                reject({
                    "err_msg": `Error!: ${xhr.status}`
                })
            }
        }
    })
};

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i=0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// export const DataRequest = (method, data_url, data_form) => {
//     const headers = new Headers();
//     headers.append('x-requested-with', 'XMLHttpRequest');

//     const requestOptions = {
//         method: method,
//         headers: headers,
//         credentials: 'same-origin'
//     }

//     if (method === 'post' && data_form) {
//         headers.append('X-CSRFToken', data_form.csrfmiddlewaretoken);
//     };

//     return fetch(data_url, requestOptions)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`Error!: ${response.status}`);
//             }
//             return response;
//         })
//         .catch(error => {
//             throw error
//         })
// }

export const getValue = ()=> {
    let elemt = (
        typeof this.selectedIndex === 'undefined' 
        ? window.event.srcElement: this
    );
    let value = elemt.value || elemt.options[elemt.selectedIndex].value;
    return value;
};

export const urlString = (url, value) => {
    const re = /(\/0\/)/;
    const dataUrl = url.replace(re, "/"+value)
    return dataUrl
};

// export {DataRequest};
// export {urlString};
// export {getCookie};