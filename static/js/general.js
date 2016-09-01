var Sidebar = React.createClass({
    componentDidMount: function() {
        /* Look up categories in semantic search.
         * For some reason they can't run locally,
         * but we'll use them with our API to
         * seperate users, problems, and blog posts.
         * For the moment though, they're together.
         */

        var dummySearchContent = [
            { title: 'Traveling Salesman Problem', description: 'Find the optimal route through a set of 500 points in 3D space.' },
            { title: 'Tron: A Postmortem', description: 'by Jake Sanders' },
            { title: 'Joshua Gruenstein', description: 'Horace Mann' }
        ];

        $('.ui.search').search({
            source: this.props.searchContent
        });
    },
    gameList: function(games, active) {
        var season = -1;
        return games.map(function(game) {
            if (game.season != season) {
                season = game.season;
                return (
                    <div key={game.id}>
                        <div className="ui horizontal divider inverted fitted">
                            {"Season " + game.season}
                        </div>
                        <a href={"/?game="+game.id} className={"item" + (active===game.id?" active":"")}>{game.name}</a>
                    </div>
                );
            } else return (
                <a href={"/?game="+game.id} className={"item" + (active===game.id?" active":"")} key={game.id}>{game.name}</a>
            );
        });
    },
    render: function() {
        return (
            <div className="ui sidebar inverted vertical menu">
                <div className="item">
                    <div className="ui fluid category search">
                        <div className="ui icon input fluid">
                            <input className="prompt" type="text" placeholder="Search..." />
                            <i className="search icon"></i>
                        </div>
                        <div className="results"></div>
                    </div>
                </div>
                <div className="item">
                    <div className="header">Games</div>
                    <div className="menu">
                        { this.gameList(this.props.games, this.props.active) }
                    </div>
                </div>
                <a href="/users" className={"item" + (this.props.active==="users"?" active":"")}>
                    Users
                </a>
                <a href="/blog" className={"item" + (this.props.active==="blog"?" active":"")}>
                    Blog
                </a>
                <div className="item">
                    <div className="header">About</div>
                    <div className="content" style={{fontSize:"0.9em",lineHeight:"1.4em"}}>NYCSL is an inter-mural programming competition for highschool students in the New York area.  Each month-ish a new problem is posted, and participants are challenged to create the optimal solution.  Challenges can be games, algorithmic problems, or something else entirely.  The top ranked students for each challenge receive prizes, and are invited to attend the NYCSL Championship at Horace Mann in the summer.</div>
                </div>
            </div>
        );
    }
});

var NavBar = React.createClass({
    componentDidMount: function() {
        $('#accountBtn').popup({
            popup: '.special.popup',
            hoverable: true,
            position : 'bottom center'
        });
    },
    openMenu: function() {
        $('.ui.sidebar').sidebar('toggle');
    },
    openLoginModal: function() {
        $('.ui.modal').modal('show');
    },
    loggedInMenu: function(githubID) {
        return (
            <div className="right menu">
                <a className="item">
                    <i className="upload icon"></i>
                    Submit
                </a>
                <a className="item">
                    <img className="ui mini circular image" id="accountBtn" src={"https://avatars0.githubusercontent.com/u/"+githubID+"?v=3&s=100"} />
                </a>
                <div className="ui special popup vertical menu" style={{width:"110px", padding:"5px 0px"}}>
                    <a className="item">
                        <i className="user icon"></i>
                        Profile
                    </a>
                    <a className="item">
                        <i className="sign out icon"></i>
                        Logout
                    </a>
                </div>
            </div>
        );
    },
    loggedOutMenu: function() {
        return (
            <div className="right menu">
                <a className="item" href="https://github.com/login/oauth/authorize?scope=user:email&client_id=787157db4920b1e60c4b">
                    <i className="sign in icon"></i>
                    Login with Github
                </a>
            </div>
        );
    },
    render: function() {
        return (
            <div className="ui secondary menu segment">
                <a className="item" href="/">
                    <b>NYCSL</b>
                </a>
                <a className="item" id="sidebarBtn" onClick={this.openMenu}>
                    <i className="sidebar icon"></i> Menu
                </a>
                { this.props.logState ? this.loggedInMenu(this.props.githubID) : this.loggedOutMenu() }
            </div>
        );
    }
});

$.get('http://' + location.hostname + ':5000/problems', function (result) {
    $.get('http://' + location.hostname + ':5000/search', function (content) {
        ReactDOM.render(
            <Sidebar games={result} active={document.body.id} searchContent={content} />,
            document.getElementById('sidebarBox')
        );
    });
});

ReactDOM.render(
    <NavBar githubID="7736334" logState={false} />,
    document.getElementById('navbarBox')
);
