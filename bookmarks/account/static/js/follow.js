const csrftoken = Cookies.get('csrftoken');

document.addEventListener('DOMContentLoaded', event => {
    // const url = '{% url "user_follow" %}';
    followAction();
});

followAction = () => {
    
    let followButton = document.querySelector('a.follow');
    
    let options = {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        mode: 'same-origin'
    };

    followButton.addEventListener('click', e => {
        e.preventDefault();
    
        // Creacion del cuerpo del request
        let formData = new FormData();
        formData.append('id', followButton.dataset.id);
        formData.append('action', followButton.dataset.action);
        options['body'] = formData;
    
        // Envio del http request
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if(data['status'] === 'ok'){
                    let previousAction = followButton.dataset.action;
    
                    // toggle del boton
                    let action = previousAction === 'follow' ? 'unfollow' : 'follow';
                    followButton.dataset.action = action;
                    followButton.innerHTML = action;
    
                    // Actualizar numero de seguidores
                    let followerCount = document.querySelector('span.count .total');
                    let totalFollowers = parseInt(followerCount.innerHTML);
    
                    followerCount.innerHTML = previousAction === 'follow' ? totalFollowers + 1 : totalFollowers - 1;
                }
            });
    });

}


