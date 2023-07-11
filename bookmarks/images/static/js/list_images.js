let page = 1;
let emptyPage = false;
let blockRequest = false;

document.addEventListener('DOMContentLoaded', event => {
    scrollAction();
});

scrollAction = () => {
    let emptyPage = false;
    let blockRequest = false;
    let page = 1;
  
    const loadMoreImages = () => {
      const margin = document.body.clientHeight - window.innerHeight - 200;
      if (window.scrollY > margin && !emptyPage && !blockRequest) {
        blockRequest = true;
        page += 1;
  
        fetch(`?images_only=1&page=${page}`)
          .then(response => response.text())
          .then(html => {
            if (html === '') {
              emptyPage = true;
            } else {
              const imageList = document.getElementById('image-list');
              imageList.insertAdjacentHTML('beforeEnd', html);
              blockRequest = false;
            }
          });
      }
    };
  
    // Add scroll event listener
    window.addEventListener('scroll', loadMoreImages);
  
    // Trigger initial scroll event
    loadMoreImages();
  };


// scrollAction = () => {
//     window.addEventListener('scroll', function(e) {

//       let margin = document.body.clientHeight - window.innerHeight - 200;

//       if(window.pageYOffset > margin && !emptyPage && !blockRequest) {
//         blockRequest = true;
//         page += 1;
    
//         fetch('?images_only=1&page=' + page)
//             .then(response => response.text())
//             .then(html => {
//                 if (html === '') {
//                     emptyPage = true;
//                 } else {
//                     let imageList = document.getElementById('image-list');
//                     imageList.insertAdjacentHTML('beforeEnd', html);
//                     blockRequest = false;
//                 }
//             });
//       }

//     });
    
//     // Launch scroll event
//     const scrollEvent = new Event('scroll');
//     window.dispatchEvent(scrollEvent);
// }
