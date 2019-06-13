:begin

CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'0'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'1'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'2'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'3'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'4'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'5'});
CREATE (n:Object {descriptive:'1,htu21d,humidity,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'1,RH,0,100,1', code:'6'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'7'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'8'});
CREATE (n:Object {descriptive:'1,htu21d,humidity,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'1,RH,0,100,1', code:'9'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'10'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'11'});
:commit
:begin

MATCH(n:Object) WHERE n.code = '0' CREATE (i:Instance {code:'0:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '1' CREATE (i:Instance {code:'1:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '2' CREATE (i:Instance {code:'2:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '3' CREATE (i:Instance {code:'3:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '4' CREATE (i:Instance {code:'4:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '5' CREATE (i:Instance {code:'5:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '6' CREATE (i:Instance {code:'6:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '7' CREATE (i:Instance {code:'7:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '8' CREATE (i:Instance {code:'8:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '9' CREATE (i:Instance {code:'9:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '10' CREATE (i:Instance {code:'10:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '11' CREATE (i:Instance {code:'11:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
:commit
:begin

MATCH(a:Instance), (b:Instance) WHERE a.code = '0:0' AND b.code='5:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='8:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='4:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '3:0' AND b.code='4:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '4:0' AND b.code='5:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '4:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '9:0' AND b.code='11:0' MERGE (a) - [:LINKED]->(b);
:commit
:begin

:commit
:begin

:commit
:begin
UNWIND [1] AS comm WITH comm MATCH(n:Instance) WHERE n.community = comm WITH n, comm OPTIONAL MATCH (n)-[r:LINKED]-(n2:Instance) WHERE n2.community = comm WITH n, n2 WHERE n2 is null WITH collect(n.code) as nodes UNWIND nodes as single_node MATCH(n3:Instance)-[:LINKED]-(n4:Instance) WHERE n3.code = single_node WITH single_node, n4.community as comm, count(n4.community) as listone WITH single_node, collect({community: comm, value:listone}) as biglistone UNWIND biglistone as element WITH single_node,MAX(element.value) as result, biglistone WITH single_node, result, filter(element in biglistone WHERE element.value = result) as the_one MATCH(n:Instance) WHERE n.code = single_node SET n.community = the_one[0].community;
:commit
:begin
MATCH(n:Instance) WHERE not (n)-[:LINKED]-() DETACH DELETE  n;
:commit
