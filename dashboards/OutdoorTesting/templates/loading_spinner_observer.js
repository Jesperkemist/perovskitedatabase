// Select the node that will be observed for mutations (loading spinner)
document.addEventListener('DOMContentLoaded', function () {
  const loadingSpinnerNode = document.getElementById('loadingSpinnerInvoker');
  
  // Options for the observer (which mutations to observe)
  const config = { attributes: true };
  
  // Callback function to execute when mutations are observed
  const callback = function(mutationsList, observer) {
      // Use traditional 'for loops' for IE 11
    for(const mutation of mutationsList) {
      if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
          var isLoading = mutation.target.style.visibility == 'hidden' ? false : true;  
          parent.postMessage(JSON.stringify({ isLoading }), '*')
      }
    }
  };
  
  // Create an observer instance linked to the callback function
  const mutationObserver = new MutationObserver(callback);
  
  // Start observing the target node for configured mutations
  mutationObserver.observe(loadingSpinnerNode, config);
})
