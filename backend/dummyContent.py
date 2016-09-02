from pymongo import MongoClient
import json

USERS_JSON = '''[{"_id" : "truell20","name" : "truell20","joinDate" : "9-2-16","schoolID" : "HM"}, {"_id" : "flyinggraysons","name" : "flyinggraysons","joinDate" : "9-1-16","schoolID" : "HM"}, {"_id" : "joshuagruenstein","name" : "joshuagruenstein","joinDate" : "9-1-16","schoolID" : "DA"}]'''
ENTRIES_JSON = '''[{"user" : {"id" : 1.0,"username" : "joshuagruenstein","name" : "Joshua Gruenstein","school" : {"id" : "HM","name" : "Horace Mann"}},"rank" : 1.0,"score" : 44.0,"events" : [ {"type" : "upload","event" : "New bot uploaded","time" : "2016-07-02T18:01:27.113Z"}, {"type" : "game-playable","event" : "Tie against Henry Hunt","time" : "2016-07-02T18:01:27.113Z","id" : 123.0}]}, {"user" : {"id" : 2.0,"username" : "truell20","name" : "Michael Truell","school" : {"id" : "DA","name" : "Dalton"}},"rank" : 2.0,"score" : 33.0,"events" : [ {"type" : "upload","event" : "New bot uploaded","time" : "2016-07-02T18:01:27.113Z"}, {"type" : "game-playable","event" : "Won against Henry Hunt","time" : "2016-07-02T18:01:27.113Z","id" : 456.0}]},{"user" : {"id" : 3.0,"username" : "flying.graysons","name" : "Henry Wildermuth","school" : {"id" : "HM","name" : "Horace Mann"}},"rank" : 3.0,"score" : 33.0,"events" : [ {"type" : "upload","event" : "New bot uploaded","time" : "2016-07-02T18:01:27.113Z"}, {"type" : "game-playable","event" : "Lost against Henry Hunt","time" : "2016-07-02T18:01:27.113Z","id" : 789.0}]}]'''
PROBLEMS_JSON = '''[{"id" : "ST","season" : 0.0,"name" : "Steiner Tree","desc" : "Find the shortest interconnection for a given set of points.","links" : [ {"url" : "/blog?steiner-tree","txt" : "Learn More"}, {"url" : "/blog?steiner-tree-tutorial","txt" : "Tutorials"}]},{"id" : "TR","name" : "Tron","season" : 0.0,"desc" : "Create a winning AI for the video game Tron.","links" : [ {"url" : "http://csclub.uwaterloo.ca/contest","txt" : "Original Competition"}]},{"id" : "TS","name" : "Traveling Salesman","season" : 0.0,"desc" : "Find the optimal route through a set of 500 points in 3D space.","links" : [ {"url" : "/blog/steiner-tree","txt" : "Learn More"}, {"url" : "/blog?steiner-tree-tutorial","txt" : "Tutorials"}]},{"id" : "RM","name" : "Roommate","season" : 0.0,"desc" : "Pair similar roommates together in the most optimal way.","links" : [ {"url" : "/blog/steiner-tree","txt" : "Learn More"}, {"url" : "/blog?steiner-tree-tutorial","txt" : "Tutorials"}]}]'''
BLOG_JSON = '''[{"_id" : "tron-post-mortem","url" : "tron-post-mortem","title" : "Tron: A Post-Mortem","author" : {"username" : "joshuagruenstein","name" : "Joshua Gruenstein"},"date" : "June 21, 2016","body" : "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam iaculis nulla eget lacus lacinia, et blandit dui hendrerit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam sit amet sem sed nisi scelerisque hendrerit. Fusce laoreet erat ex, vitae maximus lorem commodo dictum. Etiam pretium quis diam quis rutrum. Etiam laoreet commodo gravida. Suspendisse dapibus lorem quis dolor euismod laoreet. Integer dignissim ligula eu rutrum lacinia. Sed facilisis maximus risus, rutrum viverra risus maximus sed. Quisque congue nulla eros, eu facilisis lorem consectetur sit amet. Pellentesque dolor nulla, tincidunt vel arcu vitae, porta tempus ex. Vivamus tempor dolor in ligula feugiat porta. Nullam at suscipit nibh. Quisque placerat ornare nulla eu mattis. Maecenas eu velit mollis, posuere quam quis, lacinia magna.</p><p>Fusce varius sed lacus eget tristique. Donec sodales, lorem non auctor gravida, ligula lorem laoreet sem, at posuere justo turpis varius felis. Suspendisse lobortis, nibh at blandit rhoncus, nisi velit vulputate dolor, ut aliquam mi nisl et enim. Donec quis ipsum nunc. Quisque felis felis, egestas sit amet magna sit amet, fringilla malesuada lorem. Quisque sit amet sapien interdum, malesuada metus nec, tristique purus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque justo dolor, ullamcorper ac urna id, ornare blandit quam. Praesent eu ultricies nisi. Curabitur sollicitudin sed nibh et gravida. Phasellus magna metus, tincidunt vel diam at, suscipit iaculis nisl. Duis non nulla a tellus molestie pharetra. Curabitur vulputate tortor purus, ac interdum eros placerat vitae. Fusce faucibus gravida nisl pulvinar tempor. Proin at leo dictum, auctor tortor non, auctor ex. Maecenas lacinia interdum urna, quis tincidunt elit aliquam eget.</p>"},{"_id" : "tsp-description","url" : "tsp-description","title" : "TSP","author" : {"username" : "flyinggraysons","name" : "Henry Wildermuth"},"date" : "August 31, 2016","body" : "<h3>Problem Description</h3>/n/n<p>In the Traveling Salesman Problem (TSP), you are given a set of points and your goal is to create a route to visit all of them and return to the first city such that the total distance is as small as possible.</p>/n/n<p>In this version of TSP, you will be given a set of points in 3D space. These points all have integer coordinates between -100 and 100. Each point also comes with an index, which you will use for ordering the points.</p>/n/n<h3>Problem Specifics</h3>/n/n<p>The input file will be in the format:</p>/n/n<pre>/nindex-1 x-1 y-1 z-1/nindex-2 x-2 y-2 z-2/nindex-3 x-3 y-3 z-3/n.../nindex-500 x-500 y-500 z-500/n</pre>/n/n<p>You will output a list of the indices of the points to visit in order. The indices should be whitespace-separated integers. An acceptable file would look like:</p>/n/n<pre>/nindex-1 index-2 index-3 index-4 index-5 ... index-500/n</pre>/n/n<p>To aid you with the problem, we are providing starter packages which can be found <a href=/quoteproblems/starterpackages/TSP.zip/quote download>here</a>.  The input file can be found <a href=/quoteproblems/input/tsp.txt/quote download>here</a>.</p>/n/n<h3>Rules</h3>/n<p>You can use anything on wikipedia for reference. Use of the internet for algorithmic purposes is acceptable, but you may not copy and paste code from the internet. Use of websites such as StackOverflow, python.org, the Java API, and cplusplus.com is encouraged.  Collaboration between students is encouraged, but your solutions should be your own.</p>"},{"_id" : "rm-description","url" : "rm-description","title" : "Roomate Problem","author" : {"username" : "flyinggraysons","name" : "Henry Wildermuth"},"date" : "March 11, 2016","body" : "<h3>Problem Description</h3>/n/n<p>The objective of this month's competition is to group 5000 people in rooms by the common letters in their names. Each person can only be in one room, each room must have 4 people, and every person must be accounted for.  Your goal is to organize roommates such that the total RoomSum is as large as possible.  The total RoomSum is calculated by:</p>/n/n<ol>/n<li>Finding the number of letters which are present in the names of all of the people in the room. Letters are only counted multiple times if they exist that number of times in <span style=/quotetext-decoration:underline;/quote>every</span> member of the room.</li>/n<li>Summing the RoomSums of all the rooms to obtain the total RoomSum.</li>/n</ol>/n/n<h3>Problem Specifics</h3>/n/n<p>The input file will be in the format:</p>/n/n<pre>/nname1/nname2/nname3/n.../nname5000/n</pre>/n/n<p>You will create a list of the roommates that you want to pair. An acceptable file would look like:</p>/n/n<pre>/nYour Name/nroommate1-1 roommate1-2 roommate1-3 roommate1-4/nroommate2-1 roommate2-2 roommate2-3 roommate2-4/nroommate3-1 roommate3-2 roommate3-3 roommate3-4/n.../nroommateN-n roommateN-2 roommateN-3 roommateN-n/n</pre>/n/n<p>To aid you with the problem, we are providing starter packages which can be found <a href=/quoteproblems/starterpackages/RM.zip/quote download>here</a> for Java, C++ and Python.  The input file can be found <a href=/quoteproblems/input/rm.txt/quote download>here</a>. Good luck!</p>/n/n<h3>Rules</h3>/n<p>You can use anything on Wikipedia for reference. Use of the internet for algorithmic purposes is acceptable, but you may not copy and paste code. Use of websites such as StackOverflow, python.org, the Java API, and cplusplus.com is encouraged. Collaboration between students is encouraged, but your solutions should be your own.</p>"}]'''
BLOG = [{'_id': 'tron-post-mortem', 'body': '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam iaculis nulla eget lacus lacinia, et blandit dui hendrerit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam sit amet sem sed nisi scelerisque hendrerit. Fusce laoreet erat ex, vitae maximus lorem commodo dictum. Etiam pretium quis diam quis rutrum. Etiam laoreet commodo gravida. Suspendisse dapibus lorem quis dolor euismod laoreet. Integer dignissim ligula eu rutrum lacinia. Sed facilisis maximus risus, rutrum viverra risus maximus sed. Quisque congue nulla eros, eu facilisis lorem consectetur sit amet. Pellentesque dolor nulla, tincidunt vel arcu vitae, porta tempus ex. Vivamus tempor dolor in ligula feugiat porta. Nullam at suscipit nibh. Quisque placerat ornare nulla eu mattis. Maecenas eu velit mollis, posuere quam quis, lacinia magna.</p><p>Fusce varius sed lacus eget tristique. Donec sodales, lorem non auctor gravida, ligula lorem laoreet sem, at posuere justo turpis varius felis. Suspendisse lobortis, nibh at blandit rhoncus, nisi velit vulputate dolor, ut aliquam mi nisl et enim. Donec quis ipsum nunc. Quisque felis felis, egestas sit amet magna sit amet, fringilla malesuada lorem. Quisque sit amet sapien interdum, malesuada metus nec, tristique purus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque justo dolor, ullamcorper ac urna id, ornare blandit quam. Praesent eu ultricies nisi. Curabitur sollicitudin sed nibh et gravida. Phasellus magna metus, tincidunt vel diam at, suscipit iaculis nisl. Duis non nulla a tellus molestie pharetra. Curabitur vulputate tortor purus, ac interdum eros placerat vitae. Fusce faucibus gravida nisl pulvinar tempor. Proin at leo dictum, auctor tortor non, auctor ex. Maecenas lacinia interdum urna, quis tincidunt elit aliquam eget.</p>', 'author': {'name': 'Joshua Gruenstein', 'username': 'joshuagruenstein'}, 'title': 'Tron: A Post-Mortem', 'date': 'June 21, 2016', 'url': 'tron-post-mortem'}, {'_id': 'tsp-description', 'body': '<h3>Problem Description</h3>\n\n<p>In the Traveling Salesman Problem (TSP), you are given a set of points and your goal is to create a route to visit all of them and return to the first city such that the total distance is as small as possible.</p>\n\n<p>In this version of TSP, you will be given a set of points in 3D space. These points all have integer coordinates between -100 and 100. Each point also comes with an index, which you will use for ordering the points.</p>\n\n<h3>Problem Specifics</h3>\n\n<p>The input file will be in the format:</p>\n\n<pre>\nindex-1 x-1 y-1 z-1\nindex-2 x-2 y-2 z-2\nindex-3 x-3 y-3 z-3\n...\nindex-500 x-500 y-500 z-500\n</pre>\n\n<p>You will output a list of the indices of the points to visit in order. The indices should be whitespace-separated integers. An acceptable file would look like:</p>\n\n<pre>\nindex-1 index-2 index-3 index-4 index-5 ... index-500\n</pre>\n\n<p>To aid you with the problem, we are providing starter packages which can be found <a href=\"problems/starterpackages/TSP.zip\" download>here</a>.  The input file can be found <a href=\"problems/input/tsp.txt\" download>here</a>.</p>\n\n<h3>Rules</h3>\n<p>You can use anything on wikipedia for reference. Use of the internet for algorithmic purposes is acceptable, but you may not copy and paste code from the internet. Use of websites such as StackOverflow, python.org, the Java API, and cplusplus.com is encouraged.  Collaboration between students is encouraged, but your solutions should be your own.</p>', 'author': {'name': 'Henry Wildermuth', 'username': 'flyinggraysons'}, 'title': 'TSP', 'date': 'August 31, 2016', 'url': 'tsp-description'}, {'_id': 'rm-description', 'body': "<h3>Problem Description</h3>\n\n<p>The objective of this month's competition is to group 5000 people in rooms by the common letters in their names. Each person can only be in one room, each room must have 4 people, and every person must be accounted for.  Your goal is to organize roommates such that the total RoomSum is as large as possible.  The total RoomSum is calculated by:</p>\n\n<ol>\n<li>Finding the number of letters which are present in the names of all of the people in the room. Letters are only counted multiple times if they exist that number of times in <span style=\"text-decoration:underline;\">every</span> member of the room.</li>\n<li>Summing the RoomSums of all the rooms to obtain the total RoomSum.</li>\n</ol>\n\n<h3>Problem Specifics</h3>\n\n<p>The input file will be in the format:</p>\n\n<pre>\nname1\nname2\nname3\n...\nname5000\n</pre>\n\n<p>You will create a list of the roommates that you want to pair. An acceptable file would look like:</p>\n\n<pre>\nYour Name\nroommate1-1 roommate1-2 roommate1-3 roommate1-4\nroommate2-1 roommate2-2 roommate2-3 roommate2-4\nroommate3-1 roommate3-2 roommate3-3 roommate3-4\n...\nroommateN-n roommateN-2 roommateN-3 roommateN-n\n</pre>\n\n<p>To aid you with the problem, we are providing starter packages which can be found <a href=\"problems/starterpackages/RM.zip\" download>here</a> for Java, C++ and Python.  The input file can be found <a href=\"problems/input/rm.txt\" download>here</a>. Good luck!</p>\n\n<h3>Rules</h3>\n<p>You can use anything on Wikipedia for reference. Use of the internet for algorithmic purposes is acceptable, but you may not copy and paste code. Use of websites such as StackOverflow, python.org, the Java API, and cplusplus.com is encouraged. Collaboration between students is encouraged, but your solutions should be your own.</p>", 'author': {'name': 'Henry Wildermuth', 'username': 'flyinggraysons'}, 'title': 'Roomate Problem', 'date': 'March 11, 2016', 'url': 'rm-description'}]

MongoClient().drop_database('nycsl')
db = MongoClient().nycsl
db.user.insert(json.loads(USERS_JSON))
db.entries.insert(json.loads(ENTRIES_JSON))
db.problem.insert(json.loads(PROBLEMS_JSON))
db.blog.insert(BLOG)
