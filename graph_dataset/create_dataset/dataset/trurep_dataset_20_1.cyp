:begin

CREATE (n:Object {descriptive:'1,htu21d,humidity,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'1,RH,0,100,1', code:'0'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'1'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'2'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'3'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'4'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'5'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'6'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'7'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'8'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'9'});
CREATE (n:Object {descriptive:'1,htu21d,humidity,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'1,RH,0,100,1', code:'10'});
CREATE (n:Object {descriptive:'1,htu21d,humidity,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'1,RH,0,100,1', code:'11'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'12'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'13'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'14'});
CREATE (n:Object {descriptive:'4,htu21d,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf', technical:'4,C,-40,125,4', code:'15'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'16'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'17'});
CREATE (n:Object {descriptive:'2,bmp180,pressure,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'2,hPa,300,1100,2', code:'18'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'19'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'20'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'21'});
CREATE (n:Object {descriptive:'3,bmp180,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf', technical:'3,C,-40,85,3', code:'22'});
CREATE (n:Object {descriptive:'5,tsys01,temperature,https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf', technical:'5,C,-40,125,5', code:'23'});
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
MATCH(n:Object) WHERE n.code = '12' CREATE (i:Instance {code:'12:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '13' CREATE (i:Instance {code:'13:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '14' CREATE (i:Instance {code:'14:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '15' CREATE (i:Instance {code:'15:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '16' CREATE (i:Instance {code:'16:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '17' CREATE (i:Instance {code:'17:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '18' CREATE (i:Instance {code:'18:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '19' CREATE (i:Instance {code:'19:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '20' CREATE (i:Instance {code:'20:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '21' CREATE (i:Instance {code:'21:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '22' CREATE (i:Instance {code:'22:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
MATCH(n:Object) WHERE n.code = '23' CREATE (i:Instance {code:'23:0',community:'1'}) MERGE (n) - [:HAS_INSTANCE]->(i) ;
:commit
:begin

MATCH(a:Instance), (b:Instance) WHERE a.code = '0:0' AND b.code='11:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '0:0' AND b.code='12:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='3:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='4:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='7:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='9:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '1:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='5:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='17:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='19:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '2:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '3:0' AND b.code='9:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '3:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '4:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='17:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='19:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '5:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='8:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='15:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '6:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='8:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='9:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='12:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '7:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '8:0' AND b.code='10:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '8:0' AND b.code='12:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '8:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '8:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '9:0' AND b.code='11:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '9:0' AND b.code='12:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '9:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '9:0' AND b.code='22:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '10:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '10:0' AND b.code='15:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '10:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '11:0' AND b.code='12:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '11:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '11:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '12:0' AND b.code='13:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '12:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '13:0' AND b.code='15:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '13:0' AND b.code='19:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '13:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '15:0' AND b.code='16:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '15:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '17:0' AND b.code='19:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '17:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '17:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '19:0' AND b.code='21:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '19:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
MATCH(a:Instance), (b:Instance) WHERE a.code = '21:0' AND b.code='23:0' MERGE (a) - [:LINKED]->(b);
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
