const csrftoken = Cookies.get('csrftoken');

document.addEventListener('DOMContentLoaded', event => {
    // const url = '{% url "images:like" %}';'
    likeAction();
});
  
likeAction = () => {
    
    let likeButton = document.querySelector('a.like');
    
    let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };
    
    likeButton.addEventListener('click', e => {
        e.preventDefault();
        
        // add request body
        let formData = new FormData();
        formData.append('id', likeButton.dataset.id);
        formData.append('action', likeButton.dataset.action);
        options['body'] = formData;
    
        // send HTTP request
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if (data['status'] === 'ok') {
                    let previousAction = likeButton.dataset.action;
                    
                    // toggle button text and data-action
                    let action = previousAction === 'like' ? 'unlike' : 'like';
                    likeButton.dataset.action = action;
                    likeButton.innerHTML = action;
                    
                    // update like count
                    let likeCount = document.querySelector('span.count .total');
                    let totalLikes = parseInt(likeCount.innerHTML);
                    likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
                }
            });
    });
}