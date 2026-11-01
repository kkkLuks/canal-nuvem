import {createRequire} from 'module'; const require=createRequire('/home/user/hf/');
const d3=await import('/home/user/hf/node_modules/d3-geo/src/index.js');
const topo=require('topojson-client'); const fs=require('fs');
const w=JSON.parse(fs.readFileSync('/home/user/hf/node_modules/world-atlas/countries-50m.json'));
const countries=topo.feature(w,w.objects.countries);
const w1=JSON.parse(fs.readFileSync('/home/user/hf/node_modules/world-atlas/countries-110m.json'));const c110=topo.feature(w1,w1.objects.countries);
const out={};
// mundo equiretangular 1600x800
const pw=d3.geoEquirectangular().fitSize([1600,800],{type:"Sphere"});
const pathW=d3.geoPath(pw);
out.world={w:1600,h:800,paths:c110.features.map(f=>({id:f.properties.name,d:pathW(f)})).filter(x=>x.d)};
const cities={"Porto Alegre":[-51.23,-30.03],"Pelotas":[-52.34,-31.77],"Rio Grande":[-52.10,-32.03],"Montevidéu":[-56.16,-34.90],"Rio de Janeiro":[-43.17,-22.91],"São Paulo":[-46.63,-23.55],"Nova York":[-74.0,40.7],"Lisboa":[-9.14,38.72],"Paris":[2.35,48.85],"Londres":[-0.13,51.5],"Frankfurt":[8.68,50.11],"Roma":[12.5,41.9],"Tóquio":[139.7,35.7],"Joanesburgo":[28.05,-26.2],"Los Angeles":[-118.2,34.05],"Miami":[-80.2,25.8],"Lagos":[3.4,6.5],"Cidade do México":[-99.1,19.4],"Buenos Aires":[-58.4,-34.6],"Santiago":[-70.6,-33.4],"Lima":[-77.0,-12.0],"Madri":[-3.7,40.4],"Zurique":[8.54,47.37],"Hong Kong":[114.2,22.3],"Bangkok":[100.5,13.75],"Luanda":[13.23,-8.84],"Cidade do Cabo":[18.42,-33.92],"Sydney":[151.2,-33.87],"Manaus":[-60.0,-3.1],"Recife":[-34.9,-8.05],"Salvador":[-38.5,-12.97],"Brasília":[-47.9,-15.8],"Belém":[-48.5,-1.45],"Fortaleza":[-38.5,-3.7],"Curitiba":[-49.27,-25.43],"Belo Horizonte":[-43.94,-19.92],"Florianópolis":[-48.55,-27.6],"Porto Velho":[-63.9,-8.76],"Goiânia":[-49.25,-16.68],"Natal":[-35.2,-5.8],"Campo Grande":[-54.6,-20.45],"Vitória":[-40.3,-20.3]};
out.worldCities=Object.fromEntries(Object.entries(cities).map(([k,v])=>[k,pw(v)]));
// sul do Brasil / RS 1000x1000
const br=countries.features.filter(f=>["Brazil","Uruguay","Argentina","Paraguay"].includes(f.properties.name));
const rsBox={type:"Feature",geometry:{type:"Polygon",coordinates:[[[-58,-35.2],[-58,-26.5],[-48,-26.5],[-48,-35.2],[-58,-35.2]]]}};
const pr=d3.geoMercator().fitSize([1000,1000],rsBox); const pathR=d3.geoPath(pr);
out.south={w:1000,h:1000,paths:br.map(f=>({id:f.properties.name,d:pathR(f)})),cities:Object.fromEntries(Object.entries(cities).map(([k,v])=>[k,pr(v)]))};
// Brasil inteiro 1000x1000
const bra=countries.features.find(f=>f.properties.name==="Brazil");
const pb=d3.geoMercator().fitSize([1000,1000],bra); const pathB=d3.geoPath(pb);
out.brazil={w:1000,h:1000,d:pathB(bra),cities:Object.fromEntries(Object.entries(cities).map(([k,v])=>[k,pb(v)]))};
// globo ortográfico centrado no Atlântico 1000x1000
const pg=d3.geoOrthographic().rotate([30,10]).fitSize([1000,1000],{type:"Sphere"}); const pathG=d3.geoPath(pg);
out.globe={w:1000,h:1000,paths:c110.features.map(f=>pathG(f)).filter(Boolean),grat:pathG(d3.geoGraticule10()),sphere:pathG({type:"Sphere"}),cities:Object.fromEntries(Object.entries(cities).map(([k,v])=>{const c=pg(v);const vis=d3.geoDistance(v,[-30,-10])<Math.PI/2;return [k,vis?c:null]})),
 routes:{}};
for(const dest of ["Nova York","Lisboa","Paris","Londres","Frankfurt","Roma","Tóquio","Joanesburgo","Los Angeles","Miami","Lagos","Cidade do México","Buenos Aires","Santiago","Lima","Madri","Zurique","Hong Kong","Luanda","Cidade do Cabo","Bangkok","Sydney"]){
  const line={type:"LineString",coordinates:[cities["Rio de Janeiro"],cities[dest]]};
  out.globe.routes[dest]=pathG(line);
}
fs.writeFileSync('/home/user/varig/assets/maps.json',JSON.stringify(out));
console.log(Object.keys(out), JSON.stringify(out).length);
