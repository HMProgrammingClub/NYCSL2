$("#sidebarBtn").click(function(e) {
    e.preventDefault();
    $('.ui.sidebar').sidebar('toggle');
    return false;
});

$("#loginBtn").click(function(e) {
    e.preventDefault();
    $('.ui.modal').modal('show');
    return false;
});

$('#accountBtn').popup({
    popup: '.special.popup',
    hoverable: true,
    position : 'bottom center'
});


/* Look up categories in semantic search.
 * For some reason they can't run locally,
 * but we'll use them with our API to
 * seperate users, problems, and blog posts.
 * For the moment though, they're together.
 */

var dummySearchContent = [
    {
      title: 'Traveling Salesman Problem',
      description: 'Find the optimal route through a set of 500 points in 3D space.'
    },
    {
      title: 'Tron: A Postmortem',
      description: 'by Jake Sanders'
    },
    {
      title: 'Joshua Gruenstein',
      description: 'Horace Mann'
    }
];

$('.ui.search').search({
    source: dummySearchContent
});

$('.ui.dropdown').dropdown();
