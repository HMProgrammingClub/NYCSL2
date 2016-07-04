var UserProfile = React.createClass({
    formatDate: function(datetime) {
        var monthNames = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];

        var date = new Date(datetime);
        return monthNames[date.getMonth()] + ", " + date.getFullYear();
    },
    render: function() {
        return (
            <div className="item">
                <div className="ui circular small image">
                    <img src={"https://avatars0.githubusercontent.com/u/"+this.props.student.githubID+"?v=3&s=300"} />
                </div>
                <div className="content">
                    <h1 className="ui header">{ this.props.student.name }</h1>
                    <div className="meta">
                        <h3 className="ui header">{ this.props.student.school.name }</h3>
                    </div>
                    <div className="description">
                        <h3 className="ui header"><a href={"https://github.com/"+this.props.student.username+"/"}>
                            { "@" + this.props.student.username }
                        </a></h3>
                    </div>
                    <div className="extra">
                        Joined { this.formatDate(this.props.student.joinDate) }
                    </div>
                </div>
            </div>
        );
    }
});

var UserTables = React.createClass({
    render: function() {
        var seasons = this.props.seasons;
        return (
            <div>
                { Object.keys(seasons).map(function(key,i){
                    return (
                        <div key={i}>
                        { (i!=0)?<br />:<div></div> /* god I love react */ }
                        <div className="ui horizontal divider">
                            {key}
                        </div>
                        <table className="ui table unstackable">
                            <thead><tr>
                                <th>Problem</th>
                                <th>Score</th>
                                <th>School Rank</th>
                                <th>Overall Rank</th>
                            </tr></thead>
                            <tbody>
                                { seasons[key].map(function(problem,i){
                                    return (
                                        <tr key={i}>
                                        <td><a href={"/problem/"+problem.key}>{ problem.problem }</a></td>
                                        <td>{ problem.score }</td>
                                        <td>{ problem.schoolRank }</td>
                                        <td>{ problem.rank }</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                        </div>
                    );
                })}
            </div>
        );
    }
});

$.get('http://' + location.hostname + ':5000/users?userID=' + window.location.search.replace("?u=", ""), function (result) {
    ReactDOM.render(
        <UserProfile student={result} />,
        document.getElementById('userBox')
    );

    ReactDOM.render(
        <UserTables seasons={result.history} />,
        document.getElementById('seasonsBox')
    );
});
