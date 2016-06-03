var Feed = React.createClass({
    iconDict: {
        "upload" : "cloud upload icon",
        "text-upload" : "file text outline icon",
        "zip-upload" : "file archive outline icon",
        "game"   : "game icon",
        "game-playable" : "play icon",
        "bug"    : "bug icon",
        "win"    : "smile icon",
        "lose"   : "frown icon",
        "tie"    : "meh icon"
    },
    visualize: function(id) {
        alert(id)
    },
    render: function() {
        var visualize = this.visualize;
        var iconDict = this.iconDict;
        return (
            <div className={"ui flowing popup gamePopup " + this.props.id}>
                <div className="ui feed">
                    {this.props.events.map(function(feedEvent, i) {
                        return (
                            <div className="event" key={i}>
                                <div className="label">
                                    { feedEvent.id ? (
                                        <i onClick={() => visualize(feedEvent.id)} className={iconDict[feedEvent.type]}></i>
                                    ) : <i className={iconDict[feedEvent.type]}></i> }
                                </div>
                                <div className="content summary">
                                    <div className="summary">

                                        { feedEvent.event }
                                        <div className="date">
                                            { timeSince(feedEvent.time) + " ago" }
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
});

var Leaderboard = React.createClass({
    schoolList: function(obj) {
        var schools = [];
        this.props.data.forEach(function(row) {
            var exists = false;
            schools.forEach(function(school) {
                if (school.id === row.user.school.id) exists = true;
            }); if (!exists) schools.push(obj?row.user.school:row.user.school.id);
        });
        return schools;
    },
    getInitialState: function() {
        return {value:this.schoolList(false)};
    },
    handleChange: function(e) {
        //console.log(this.state)
    },
    componentDidMount: function() {
        // link rows and popups
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

        // link dropdown
        $('.ui.dropdown').dropdown({
            onChange: (value) => {
                this.setState({value});
                if (this.state.value.length < 1) {
                    this.state.value = this.schoolList(false);
                }
            }
        });
    },
    schoolSelect: function() {
        return (
            <select className="ui fluid search dropdown"
                    multiple={true} value={this.state.value} onChange={this.handleChange}>
                <option value="">Filter by School</option>
                {this.schoolList(true).map(function(school) {
                    return <option key={school.id} value={school.id}>{school.name}</option>
                })}
            </select>
        );
    },
    render: function() {
        var schoolIDs = this.state.value;
        var rows = this.props.data.filter(function(row) {
            var schoolContained = false;
            schoolIDs.forEach(function(schoolID) {
                if (row.user.school.id === schoolID) schoolContained = true;
            }); return schoolContained;
        });
        return (
            <div className="leaderboard">
                { this.schoolSelect() }
                <table className="ui table unstackable">
                    <thead><tr>
                        <th>Rank</th>
                        <th>Name</th>
                        <th>School</th>
                        <th>Score</th>
                    </tr></thead>
                    <tbody>
                        {rows.map(function(row) {
                            return (
                                <tr className={'playerRow ' +row.user.id} key={row.rank}>
                                    <td><b>{row.rank}</b></td>
                                    <td><a href={'/user/' + row.user.username}>{row.user.name}</a></td>
                                    <td>{row.user.school.name}</td>
                                    <td>{row.score}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                {rows.map(function(row) {
                    return <Feed events={row.events} id={row.user.id} key={row.rank} />
                })}
            </div>
        );
    }
});

var Jumbo = React.createClass({
    render: function() {
        return (
            <div className="row">
                <div className="row column">
                    <div className="ui huge message page grid">
                        <h1 className="ui huge header">{this.props.game}</h1>
                        <p>{this.props.desc}
                        <br />
                        {this.props.links.map(function(link, i) {
                            return <a className="ui blue basic button" style={{marginTop:"10px"}} href={link.url} key={i}>{link.txt}</a>
                        })}
                        </p>
                    </div>
                </div>
            </div>
        );
    }
});

var jumboData = {game:"Steiner Tree", desc:"Find the shortest interconnection for a given set of points.", links:[
    {url:"/blog/steiner-tree",txt:"Learn More"},
    {url:"/blog/steiner-tree-tutorial",txt:"Tutorials"}
]}

var leaderData = [
    {user: {id: 1, username: "joshuagruenstein", name: "Joshua Gruenstein", school:{id: "HM", name: "Horace Mann"}}, rank: 1, score: 44, events:[
        {type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
        {type: "game-playable", event: "Tie against Henry Hunt", time: new Date(new Date().getTime()-600000), id:123}
    ]},
    {user: {id: 2, username: "truell20", name: "Michael Truell", school:{id: "DA", name: "Dalton"}}, rank: 2, score: 33, events:[
        {type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
        {type: "game-playable", event: "Won against Henry Hunt", time: new Date(new Date().getTime()-600000), id:456}
    ]},
    {user: {id: 3, username: "flying.graysons", name: "Henry Wildermuth", school:{id: "HM", name: "Horace Mann"}}, rank: 3, score: 33, events:[
        {type: "upload", event: "New bot uploaded", time: new Date(new Date().getTime()-300000)},
        {type: "game-playable", event: "Lost against Henry Hunt", time: new Date(new Date().getTime()-600000), id:789}
    ]}
];

ReactDOM.render(
    <Leaderboard data={leaderData} />,
    document.getElementById('leaderBoard')
);

ReactDOM.render(
    <Jumbo game={jumboData.game} desc={jumboData.desc} links={jumboData.links} />,
    document.getElementById('jumboBox')
);
