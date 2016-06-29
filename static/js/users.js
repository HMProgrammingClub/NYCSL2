var QualifiedLeaderboard = React.createClass({
    render: function() {
        return (
            <table className="ui very basic celled table fluid unstackable">
                <thead><tr>
                    <th>Student</th>
                    <th>Composite Score</th>
                </tr></thead>
                <tbody>
                    {this.props.students.map(function(student) {
                        return (
                            <tr key={ student.id }>
                                <td>
                                    <h4 className="ui image header">
                                        <img src={"https://avatars0.githubusercontent.com/u/" + student.githubID + "?v=3&s=50"} className="ui mini rounded image" />
                                        <div className="content">
                                            { student.name }
                                            <div className="sub header">{ student.school.name }</div>
                                        </div>
                                    </h4>
                                </td>
                                <td>{ student.compositeScore }</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        );
    }
});

var UserGrid = React.createClass({
    schoolList: function(obj) {
        var schools = [];
        this.props.students.forEach(function(student) {
            var exists = false;
            schools.forEach(function(school) {
                if (school.id === student.school.id) exists = true;
            }); if (!exists) schools.push(obj?student.school:student.school.id);
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
    filterSchool: function(school) {
        // filter to only the given school object
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
        var students = this.props.students.filter(function(student) {
            var schoolContained = false;
            schoolIDs.forEach(function(schoolID) {
                if (student.school.id === schoolID) schoolContained = true;
            }); return schoolContained;
        });

        return (
            <div> { this.schoolSelect() } <br />
            <div className="ui four column doubling grid">
                {students.map(function(student) {
                    return (
                        <div className="column" key={student.id}>
                            <div className="ui fluid card">
                            <a className="image" href={"/users/"+student.username}>
                                <img src={"https://avatars0.githubusercontent.com/u/" + student.githubID + "?v=3&s=300"} />
                            </a>
                            <div className="content">
                                <div className="header">{ student.name }</div>
                                <div className="meta">
                                    { student.school.name }
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

var UserData = [
    { id: 3, githubID: 7736334, name: "Henry Wildermuth", school:{id: "HM", name: "Horace Mann"}, compositeScore: 22},
    { id: 4, githubID: 2452433, name: "Joshua Gruenstein", school:{id: "DA", name: "Dalton"}, compositeScore: 32}
];

// render first n elements (or all with nonzero score) of the same data
// i think it makes sense caus it lowers the number of requests
// ex:

var QualifiedData = UserData.filter(function(user) {
    return user.compositeScore != 0;
});

ReactDOM.render(
    <QualifiedLeaderboard students={QualifiedData} />,
    document.getElementById('qualifiedBox')
);

ReactDOM.render(
    <UserGrid students={UserData} />,
    document.getElementById('usersBox')
);
