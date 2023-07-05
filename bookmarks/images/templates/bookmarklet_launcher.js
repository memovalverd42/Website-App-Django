// (() => {
//     if(!window.bookmarklet) {
//         const urlBookmarklet = '//mysite.com:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999);
//         const script = document.createElement('script');
//         let bookmarklet_js = document.body.appendChild(script);
//         bookmarklet_js.src = urlBookmarklet;
//         window.bookmarklet = true;
//     } else {
//         bookmarkletLaunch();
//     }
// })();

(function(){
  if(!window.bookmarklet) {
    let bookmarklet_js = document.body.appendChild(document.createElement('script'));
    bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999);
    window.bookmarklet = true;
  }
  else {
    bookmarkletLaunch();
  }
})();