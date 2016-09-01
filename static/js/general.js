var Sidebar = React.createClass({
    componentDidMount: function() {
        $('.ui.search').search({
            apiSettings: {
           		url: 'http://' + location.hostname + ':5000/search?query={query}'
            }, type: 'category'
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
                        <a href={"/?"+game.id} className={"item" + (active===game.id?" active":"")}>{game.name}</a>
                    </div>
                );
            } else return (
                <a href={"/?"+game.id} className={"item" + (active===game.id?" active":"")} key={game.id}>{game.name}</a>
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
    signInModal: function() {
        return (
            <div className="ui modal">
                <div className="header">
                    Login with Github
                </div>
                <div className="image content">
                    <div className="description">
                        <div className="ui header">Click the button below to login with Github.</div>
                        <p>If you don't already have an account linked to your Github profile, that's ok. Well automatically detect it and help you get things set up.</p>
                    </div>
                </div>
                <div className="actions">
                    <button className="ui button fluid">
                        <i className="github icon"></i>
                        Connect to Github
                    </button>
                </div>
            </div>
        );
    },
    signUpModal: function() {
        return (
            <div className="ui modal">
                <div className="header">
                    Signup with Github
                </div>
                <div className="image content"><div className="description">
                    <div className="ui form">
                        <div className="field">
                            <label>School</label>
                            <select className="ui fluid search dropdown selection">
                                <option value="">Select School</option>
                                <option value="HM">Horace Mann School</option>
                                <option value="DA">Dalton School</option>
                                <option value="ST">Stuyvesant</option>
                            </select>
                        </div>
                    </div>
                </div></div>
                <div className="actions">
                    <button className="ui button fluid">
                        Create Account
                    </button>
                </div>
            </div>
        );
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
                <a className="item" onClick={this.openLoginModal}>
                    <i className="sign in icon"></i>
                    Login with Github
                </a>
                { this.signInModal() }
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
