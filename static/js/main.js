function linkPopups() {
    var rows = document.querySelectorAll(".playerRow");
    for (var i=0; i<rows.length; i++) {
        var className = rows[i].className;
        className = className.substr(className.indexOf(' ')+1);
        $('.playerRow.' + className).popup({
            popup:$('.gamePopup.' + className),
            hoverable:true,
            position : 'bottom right'
        });
    }
}

var PlayerRow = React.createClass({
    render: function() {
        var user = this.props.data.user;
        return (
            <tr className={'playerRow ' + user.id}>
                <td><b>{this.props.data.rank}</b></td>
                <td><a href={'/user/' + user.username}>{user.name}</a></td>
                <td>{user.school}</td>
                <td>{this.props.data.score}</td>
            </tr>
        );
    }
});

var Leaderboard = React.createClass({
    render: function() {
        return (
            <table className="ui table unstackable">
                <thead><tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>School</th>
                    <th>Score</th>
                </tr></thead>
                <tbody>
                    {this.props.data.map(function(playerRow) {
                        return <PlayerRow data={playerRow} />
                    })}
                </tbody>
            </table>
        );
    }
});

var FeedEvent = React.createClass({
    render: function() {
        return (
            <div className="event">
                <div className="label">
                    <i className={this.props.data.type === "upload" ? "file archive outline icon" : "game icon"}></i>
                </div>
                <div className="content summary">
                    <div className="summary">
                        { this.props.data.event }
                        <div className="date">
                            { timeSince(this.props.data.time) + " ago" }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var Feed = React.createClass({
    render: function() {
        return (
            <div className={"ui flowing popup gamePopup " + this.props.data.id}>
                <div className="ui feed">
                    {this.props.data.events.map(function(feedEvent) {
                        return <FeedEvent data={feedEvent} />
                    })}
                </div>
            </div>
        );
    }
});

var Feeds = React.createClass({
    render: function() {
        return (
            <div>
                {this.props.data.map(function(feed) {
                        return <Feed data={feed} />
                })}
            </div>
        );
    }
});


var leaderData = [
    {user: {id: 1, username: "joshuagruenstein", name: "Joshua Gruenstein", school: "Horace Mann"}, rank: 1, score: 44},
    {user: {id: 2, username: "truell20", name: "Michael Truell", school: "Horace Mann"}, rank: 2, score: 33}
];

var feedData = [
    {id: 1, events: [{type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
                     {type: "game", event: "Won against Henry Hunt", time: new Date(new Date().getTime()-600000)}]},
    {id: 2, events: [{type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
                     {type: "game", event: "Won against Joshua Gruenstein", time: new Date(new Date().getTime()-600000)}]}
];

var games = [
    { id:"ST", name:"Steiner Tree", season:0 },
    { id:"TR", name:"Tron", season:0 },
    { id:"RM", name:"Roommate", season:0 },
    { id:"TS", name:"Traveling Salesman", season:0 }
];

ReactDOM.render(
    <Leaderboard data={leaderData} />,
    document.getElementById('leaderBoard')
);

ReactDOM.render(
    <Feeds data={feedData} />,
    document.getElementById('feedsBox')
);

var Sidebar = React.createClass({
    gameList: function(games, active) {
        var season = -1;
        var newGames = games.map(function(game) {
            if (game.season != season) {
                season = game.season;
                return (
                    <div>
                        <div className="ui horizontal divider inverted fitted">
                            {"Season " + game.season}
                        </div>
                        <a href={"/?game="+game.id} className={"item" + (active===game.id?" active":"")}>{game.name}</a>
                    </div>
                );
            } else return (
                <a href={"/?game="+game.id} className={"item" + (active===game.id?" active":"")}>{game.name}</a>
            );
        });

        return newGames;
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
                <a className={"item" + (this.props.active==="users"?" active":"")}>
                    Users
                </a>
                <a className={"item" + (this.props.active==="blog"?" active":"")}>
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


ReactDOM.render(
    <Sidebar games={games} active="ST" />,
    document.getElementById('sidebarBox')
);

linkPopups();
