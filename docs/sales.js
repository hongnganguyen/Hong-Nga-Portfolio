/* Project 1 - Car Rental Sales Performance (6 pages). Uses the shared helpers exposed as window.BI. SYNTHETIC data only. */
(function(){
"use strict";
var B=window.BI,$=B.$,sum=B.sum,usd=B.usd,kk=B.kk,dlt=B.dlt,add=B.add,opt=B.opt,xcat=B.xcat,yval=B.yval,AX=B.AX,GR=B.GR,kpi=B.kpi,tbl=B.tbl,donut=B.donut,stacked=B.stacked,MN=B.MN,dim=B.dim,dk=B.dk,mo=B.mo,dayArr=B.dayArr;
var OR="#ff5500",CY="#5fc8d6",BLUE="#4da3ff",GREEN="#1f9e32",RED="#d92d20",INK="#111";
var G=B.D.sales;
function pc(x){return (x*100).toFixed(1)+"%";}
function days(m){var a=[];for(var d=1;d<=dim(m);d++)a.push(d);return a;}
function f2(v){return usd(v,true);}

/* ---------- aggregates ---------- */
var S={},N={},NP={},NL={},DY={},NW={},ED={},EC={},PM={},NO={},CLS={},MT={};
for(var i=1;i<=12;i++){MT[i]={s:0,n:0,d:0,c:0,w:0};CLS[i]={Premium:{s:0,n:0},Luxury:{s:0,n:0}};PM[i]={};NO[i]={n:0,s:0,c:0};EC[i]={};}
G.rent.forEach(function(r){var dt=r[0],m=mo(dt),cl=r[1],pr=r[2];
  add(S,dt,r[4]);add(N,dt,r[7]);add(cl==="Premium"?NP:NL,dt,r[7]);add(DY,dt,r[3]);add(NW,dt,r[8]);
  var t=MT[m];t.s+=r[4];t.n+=r[7];t.d+=r[3];t.c+=r[6];t.w+=r[8];
  CLS[m][cl].s+=r[4];CLS[m][cl].n+=r[7];
  if(pr==="None"){var o=NO[m];o.n+=r[7];o.s+=r[4];o.c+=r[6];}
  else{var q=PM[m][pr]=PM[m][pr]||{n:0,s:0,p:0,c:0};q.n+=r[7];q.s+=r[4];q.p+=r[5];q.c+=r[6];}});
G.exp.forEach(function(r){var m=mo(r[0]);add(ED,r[0],r[2]);add(EC[m],r[1],r[2]);});
function etot(m){var s=0;for(var k in EC[m])s+=EC[m][k];return s;}
function mm(m){var s=dayArr(S,m),e=dayArr(ED,m),p=s.map(function(x,i){return x-e[i];}),n=dayArr(N,m),d=dayArr(DY,m);
  return {s:s,e:e,p:p,n:n,d:d,q1:dayArr(NP,m),q2:dayArr(NL,m),S:sum(s),E:sum(e),P:sum(p),R:sum(n),D:sum(d)};}
var CC={"Direct cost":"#161616","Ops staff salary":"#0e4a7a","Sales salary":"#7fa8c7","Promo cost":OR,"Garage & yard":"#7a7a7a","Back office":"#19a803","Damage & loss":"#e4572e","Marketing":"#bdbdbd","Office":"#f2c94c"};
var CO=Object.keys(CC);
var PCOL={BOGO:OR,B4G4:"#1a1a1a",BSGM:"#7a7a7a",B3G2:"#bdbdbd",B2G2:"#e0e0e0",IM:"#326a96"};
function sortedPromos(m){var pm=PM[m];return Object.keys(pm).sort(function(a,b){return pm[b].s-pm[a].s;});}
function ul(items){return "<ul><li>"+items.join("</li><li>")+"</li></ul>";}
function avg(a){return a.length?sum(a)/a.length:0;}
function weekdayAvg(m,c){var s=[0,0,0,0,0,0,0],n=[0,0,0,0,0,0,0];c.s.forEach(function(v,i){var w=new Date(2025,m-1,i+1).getDay();s[w]+=v;n[w]++;});return [1,2,3,4,5,6,0].map(function(w){return n[w]?s[w]/n[w]:0;});}
var WD=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];

/* ---------- map ---------- */
function drawMap(id,m){
  var mm_=B.makeMap(id);if(!mm_)return;mm_.layer.clearLayers();
  var rows=G.bysub.filter(function(r){return r[0]===m;}),mx=Math.max.apply(null,rows.map(function(r){return r[2];}).concat([1]));
  rows.forEach(function(r){var s=G.suburbs[r[1]];
    L.circleMarker([s[1],s[2]],{radius:5+22*Math.sqrt(r[2]/mx),color:"#12b206",weight:1,fillColor:"#2fd02a",fillOpacity:.6})
      .bindTooltip(s[0]+": "+f2(r[2])+" · "+r[3]+" rentals · "+r[4]+" customers").addTo(mm_.layer);});
  setTimeout(function(){mm_.map.invalidateSize();},60);
}

/* ---------- 1 OVERVIEW ---------- */
function over(m){
  var c=mm(m),p=m>1?mm(m-1):null,dd=days(m),q1=sum(c.q1),q2=sum(c.q2);
  $("s-kpis").innerHTML=
    kpi(3,"Profit · margin "+pc(c.S?c.P/c.S:0),'<span class="'+(c.P>=0?"up":"down")+'">'+usd(c.P)+"</span>",p?dlt(c.P,p.P):null,true,c.p,OR)+
    kpi(3,"Rental sales",usd(c.S),p?dlt(c.S,p.S):null,true,c.s,CY)+
    kpi(3,"Total expenses",usd(c.E),p?dlt(c.E,p.E):null,false,c.e,"#333")+
    kpi(3,"Rentals · "+q1+" Premium / "+q2+" Luxury",c.R,p?dlt(c.R,p.R):null,true,c.n,OR);
  opt("s-salesexp",{tooltip:{trigger:"axis",valueFormatter:f2},legend:{top:0},color:[OR,INK],grid:GR,xAxis:xcat(dd),yAxis:yval(),
    series:[{name:"Rental sales",type:"bar",stack:"x",data:c.s.map(Math.round)},{name:"Total expenses",type:"bar",stack:"x",data:c.e.map(Math.round)}]});
  opt("s-profitline",{tooltip:{trigger:"axis",valueFormatter:f2},grid:GR,xAxis:xcat(dd),yAxis:yval(),
    series:[{type:"line",smooth:true,data:c.p.map(Math.round),itemStyle:{color:BLUE},areaStyle:{color:BLUE,opacity:.2},markLine:{silent:true,symbol:"none",data:[{yAxis:0}],lineStyle:{color:"#999"}},
      markPoint:{data:[{type:"max"},{type:"min"}],symbolSize:44,label:{formatter:function(q){return kk(q.value);},fontSize:10,color:"#fff"},itemStyle:{color:BLUE}}}]});
  var from=Math.max(1,m-5),cats=[],sv=[],ev=[],mg=[];
  for(var i=from;i<=m;i++){cats.push(MN[i-1]);var s=MT[i].s,e=etot(i);sv.push(Math.round(s));ev.push(Math.round(e));mg.push(s?+((s-e)/s*100).toFixed(1):0);}
  opt("s-trend6",{tooltip:{trigger:"axis"},legend:{top:0},color:[OR,INK,BLUE],grid:{left:48,right:44,top:30,bottom:26},xAxis:xcat(cats),
    yAxis:[yval(),{type:"value",axisLabel:{color:"#475467",formatter:"{value}%"},splitLine:{show:false}}],
    series:[{name:"Rental sales",type:"bar",data:sv},{name:"Total expenses",type:"bar",data:ev},{name:"Profit margin %",type:"line",yAxisIndex:1,smooth:true,data:mg,label:{show:true,formatter:"{c}%",fontSize:10}}]});
  var ec=EC[m],rows=[["Revenue",c.S]].concat(CO.map(function(k){return [k,ec[k]||0];}),[["Profit",c.P]]);
  $("s-summary").innerHTML=tbl([{t:"Item"},{t:"Amount",bar:"#ffd1ba",f:f2}],rows.map(function(r){return {v:r,bc:r[0]==="Revenue"?"#a3ddb3":r[0]==="Profit"?"#f5c4af":null};}));
  $("s-ins").innerHTML=ul(insights(m,c,p));
}
function insights(m,c,p){
  var li=[],best=c.p.indexOf(Math.max.apply(null,c.p)),worst=c.p.indexOf(Math.min.apply(null,c.p)),neg=c.p.filter(function(x){return x<0;}).length;
  if(p)li.push("Profit is <b>"+usd(c.P)+"</b> ("+pc(c.S?c.P/c.S:0)+" margin), "+(c.P>=p.P?"up ":"down ")+"<b>"+Math.abs(dlt(c.P,p.P)*100).toFixed(1)+"%</b> versus "+MN[m-2]+" while rental sales moved "+(dlt(c.S,p.S)*100).toFixed(1)+"% and expenses "+(dlt(c.E,p.E)*100).toFixed(1)+"%.");
  li.push("Best day: <b>"+MN[m-1]+" "+(best+1)+"</b> ("+usd(c.p[best])+"); weakest: <b>"+MN[m-1]+" "+(worst+1)+"</b> ("+usd(c.p[worst])+"). "+neg+" loss-making day(s): fixed salaries and garage costs are paid whether or not cars are rented.");
  var we=[],wd=[];c.s.forEach(function(v,i){var w=new Date(2025,m-1,i+1).getDay();(w===0||w===6?we:wd).push(v);});
  li.push("Weekend days average <b>"+usd(avg(we))+"</b> of rental sales versus <b>"+usd(avg(wd))+"</b> on weekdays"+(avg(we)>avg(wd)?": weekends carry the month, so keep Premium and Luxury cars available then.":": weekday demand is the stronger lever."));
  var pm=sortedPromos(m);
  if(pm.length){var P0=PM[m][pm[0]],ps=sum(pm.map(function(k){return PM[m][k].s;}));li.push("Promotions generate <b>"+pc(ps/MT[m].s)+"</b> of sales; <b>"+pm[0]+"</b> leads with "+usd(P0.s)+". See the Promotions page for margin by promotion.");}
  var cl=CLS[m];li.push("Premium cars bring <b>"+pc(cl.Premium.s/(MT[m].s||1))+"</b> of rental sales and Luxury <b>"+pc(cl.Luxury.s/(MT[m].s||1))+"</b>.");
  return li;
}

/* ---------- 2 SALES & RENTALS ---------- */
function sales(m){
  var c=mm(m),p=m>1?mm(m-1):null,dd=days(m),cl=CLS[m],avgv=c.R?c.S/c.R:0,pav=p&&p.R?p.S/p.R:null;
  $("s-skpis").innerHTML=
    kpi(3,"Rentals",c.R,p?dlt(c.R,p.R):null,true,c.n,OR)+
    kpi(3,"Rental days · avg "+(c.R?(c.D/c.R).toFixed(1):0)+" per rental",c.D,p?dlt(c.D,p.D):null,true,c.d,CY)+
    kpi(3,"Average rental value",usd(avgv,true),pav?dlt(avgv,pav):null,true,c.s.map(function(v,i){return c.n[i]?v/c.n[i]:0;}),"#333")+
    kpi(3,"Premium share of sales",pc(cl.Premium.s/(c.S||1)),p?dlt(cl.Premium.s/(c.S||1),CLS[m-1].Premium.s/(MT[m-1].s||1)):null,true);
  opt("s-qty",{tooltip:{trigger:"axis"},legend:{top:0},color:[OR,INK],grid:GR,xAxis:xcat(dd),yAxis:yval(),
    series:[{name:"Premium rentals",type:"bar",stack:"q",data:c.q1,label:{show:true,color:"#fff",fontSize:9}},{name:"Luxury rentals",type:"bar",stack:"q",data:c.q2,label:{show:true,color:"#fff",fontSize:9}}]});
  donut("s-clsdonut",[{name:"Premium",value:+cl.Premium.s.toFixed(2)},{name:"Luxury",value:+cl.Luxury.s.toFixed(2)}],usd(c.S),{Premium:OR,Luxury:INK});
  var wa=weekdayAvg(m,c),best=wa.indexOf(Math.max.apply(null,wa));
  opt("s-wday",{tooltip:{valueFormatter:f2},grid:GR,xAxis:xcat(WD),yAxis:yval(),series:[{type:"bar",data:wa.map(function(v,i){return {value:Math.round(v),itemStyle:{color:i===best?OR:"#ffb08a"}};}),label:{show:true,position:"top",formatter:function(q){return kk(q.value);},fontSize:10}}]});
  var dur=[0,0,0,0,0,0,0,0];G.dur.forEach(function(r){if(r[0]===m)dur[r[1]]=r[2];});
  opt("s-dur",{tooltip:{trigger:"axis"},grid:GR,xAxis:xcat(["1 day","2 days","3 days","4 days","5 days","6 days","7 days"]),yAxis:yval(),series:[{name:"Rentals",type:"bar",data:dur.slice(1),itemStyle:{color:CY},label:{show:true,position:"top",fontSize:10}}]});
  var cats=MN.slice(),pr=[],lu=[];for(var i=1;i<=12;i++){pr.push(Math.round(CLS[i].Premium.s));lu.push(Math.round(CLS[i].Luxury.s));}
  stacked("s-clsm",cats,[["Premium",pr],["Luxury",lu]],[OR,INK]);
}

/* ---------- 3 PROMOTIONS ---------- */
function promo(m){
  var pm=PM[m],no=NO[m],names=sortedPromos(m),t=MT[m],ps=sum(names.map(function(k){return pm[k].s;})),pcst=sum(names.map(function(k){return pm[k].p;})),pcos=sum(names.map(function(k){return pm[k].c;}));
  var mgP=ps?(ps-pcos-pcst)/ps:0,mgN=no.s?(no.s-no.c)/no.s:0,prev=m>1?PM[m-1]:null,ps0=prev?sum(Object.keys(prev).map(function(k){return prev[k].s;})):0;
  $("s-pkpis").innerHTML=
    kpi(3,"Promo share of sales",pc(ps/(t.s||1)),m>1&&ps0?dlt(ps/(t.s||1),ps0/(MT[m-1].s||1)):null,true)+
    kpi(3,"Promo cost",usd(pcst),prev?dlt(pcst,sum(Object.keys(prev).map(function(k){return prev[k].p;}))):null,false)+
    kpi(3,"Promo cost as % of promo sales",pc(ps?pcst/ps:0))+
    '<div class="card kpi c3 two"><div><div class="l">Margin · promo</div><div class="v '+(mgP>=mgN?"up":"down")+'">'+pc(mgP)+'</div></div><div><div class="l">Margin · full price</div><div class="v">'+pc(mgN)+"</div></div></div>";
  $("s-promotbl").innerHTML=tbl([{t:"Promotion"},{t:"Rentals"},{t:"Promo cost",bar:OR,f:f2},{t:"Direct cost",f:f2},{t:"Sales",bar:OR,f:f2},{t:"Profit",bar:"#6f95b3",f:f2},{t:"Margin",f:function(v){return '<span class="'+(v>=mgN?"up":"down")+'">'+pc(v)+"</span>";}}],
    names.map(function(k){var o=pm[k];return {v:[k,o.n,o.p,o.c,o.s,o.s-o.c-o.p,o.s?(o.s-o.c-o.p)/o.s:0]};}));
  donut("s-promodonut",names.map(function(k){return {name:k,value:+pm[k].s.toFixed(2)};}),usd(ps),PCOL);
  var mg=names.map(function(k){return pm[k].s?+(((pm[k].s-pm[k].c-pm[k].p)/pm[k].s)*100).toFixed(1):0;});
  opt("s-promomargin",{tooltip:{valueFormatter:function(v){return v+"%";}},grid:GR,xAxis:xcat(names),yAxis:yval(function(v){return v+"%";}),
    series:[{type:"bar",data:mg.map(function(v){return {value:v,itemStyle:{color:v>=mgN*100?GREEN:"#ff9a66"}};}),label:{show:true,position:"inside",formatter:"{c}%",fontSize:11,color:"#111"},
      markLine:{symbol:"none",silent:true,data:[{yAxis:+(mgN*100).toFixed(1),name:"Full price"}],label:{formatter:"Full-price margin {c}%",position:"insideStartTop",color:"#111"},lineStyle:{color:"#111",type:"dashed"}}}]});
  var sh=[];for(var i=1;i<=12;i++){var pi=PM[i],s=sum(Object.keys(pi).map(function(k){return pi[k].s;}));sh.push(+(s/(MT[i].s||1)*100).toFixed(1));}
  opt("s-promoshare",{tooltip:{trigger:"axis",valueFormatter:function(v){return v+"%";}},grid:GR,xAxis:xcat(MN),yAxis:yval(function(v){return v+"%";}),
    series:[{type:"line",smooth:true,data:sh,itemStyle:{color:OR},areaStyle:{color:OR,opacity:.15},markPoint:{data:[{coord:[m-1,sh[m-1]],value:sh[m-1]}],symbolSize:46,label:{formatter:function(q){return q.value+"%";},color:"#fff",fontSize:10},itemStyle:{color:OR}}}]});
  var li=[];
  if(names.length){var topn=names[0],bm=names.slice().sort(function(a,b){return mg[names.indexOf(b)]-mg[names.indexOf(a)];}),low=names.filter(function(k,i){return mg[i]<mgN*100;});
    li.push("<b>"+topn+"</b> is the biggest promotion ("+usd(pm[topn].s)+", "+pc(pm[topn].s/(ps||1))+" of promo sales) with a margin of <b>"+mg[0]+"%</b> versus <b>"+pc(mgN)+"</b> on full-price rentals.");
    li.push("Highest-margin promotion: <b>"+bm[0]+"</b> ("+mg[names.indexOf(bm[0])]+"%). "+(low.length?"Below the full-price margin: <b>"+low.join(", ")+"</b>: tighten the discount or restrict to low-demand days.":"Every promotion still earns at least the full-price margin this month."));
    li.push("Promotions cost <b>"+usd(pcst)+"</b> ("+pc(ps?pcst/ps:0)+" of promo sales). Judge a promotion by the profit it adds, not by rental count: promo rentals "+(mgP>=mgN?"also hold the margin":"dilute the margin by "+((mgN-mgP)*100).toFixed(1)+" points")+" this month.");}
  $("s-promoins").innerHTML=ul(li);
}

/* ---------- 4 CUSTOMERS & LOCATION ---------- */
function cust(m){
  var t=MT[m],cr=G.cust[m-1],pcr=m>1?G.cust[m-2]:null,pt=m>1?MT[m-1]:null,rep=t.n?(t.n-t.w)/t.n:0,prep=pt&&pt.n?(pt.n-pt.w)/pt.n:null;
  $("s-ckpis").innerHTML=
    kpi(3,"Unique customers",cr[1],pcr?dlt(cr[1],pcr[1]):null,true)+
    kpi(3,"New customers",t.w,pt?dlt(t.w,pt.w):null,true)+
    kpi(3,"Returning-customer rentals",pc(rep),prep!=null?dlt(rep,prep):null,true)+
    kpi(3,"Rentals per customer",(cr[1]?t.n/cr[1]:0).toFixed(2));
  drawMap("s-map",m);
  var rows=G.bysub.filter(function(r){return r[0]===m;}).sort(function(a,b){return b[2]-a[2];}),tot=sum(rows.map(function(r){return r[2];}))||1;
  $("s-suburbtbl").innerHTML=tbl([{t:"Suburb"},{t:"Rentals"},{t:"Sales",bar:"#2fd02a",f:f2},{t:"Share",f:function(v){return pc(v);}}],rows.map(function(r){return {v:[G.suburbs[r[1]][0],r[3],r[2],r[2]/tot]};}));
  var nw=[],rt=[];for(var i=1;i<=12;i++){nw.push(MT[i].w);rt.push(MT[i].n-MT[i].w);}
  opt("s-newret",{tooltip:{trigger:"axis"},legend:{top:0},color:[CY,OR],grid:GR,xAxis:xcat(MN),yAxis:yval(),
    series:[{name:"Rentals by new customers",type:"bar",stack:"c",data:nw},{name:"Rentals by returning customers",type:"bar",stack:"c",data:rt}]});
  var top=rows.slice(0,12),cum=0,cp=top.map(function(r){cum+=r[2];return +(cum/tot*100).toFixed(1);});
  opt("s-pareto",{tooltip:{trigger:"axis"},legend:{top:0},color:[OR,INK],grid:{left:48,right:44,top:30,bottom:46},xAxis:{type:"category",data:top.map(function(r){return G.suburbs[r[1]][0];}),axisLabel:{color:"#475467",rotate:35,fontSize:10},axisLine:AX.axisLine,axisTick:AX.axisTick},
    yAxis:[yval(),{type:"value",max:100,axisLabel:{color:"#475467",formatter:"{value}%"},splitLine:{show:false}}],
    series:[{name:"Sales",type:"bar",data:top.map(function(r){return Math.round(r[2]);})},{name:"Cumulative share",type:"line",yAxisIndex:1,smooth:true,data:cp,label:{show:true,formatter:"{c}%",fontSize:9}}]});
}

/* ---------- 5 PROFIT & COSTS ---------- */
function profit(m){
  var c=mm(m),p=m>1?mm(m-1):null,dd=days(m),ec=EC[m];
  $("s-fkpis").innerHTML=
    kpi(3,"Revenue",usd(c.S),p?dlt(c.S,p.S):null,true,c.s,CY)+
    kpi(3,"Total expenses",usd(c.E),p?dlt(c.E,p.E):null,false,c.e,"#333")+
    kpi(3,"Profit",'<span class="'+(c.P>=0?"up":"down")+'">'+usd(c.P)+"</span>",p?dlt(c.P,p.P):null,true,c.p,OR)+
    kpi(3,"Profit margin",pc(c.S?c.P/c.S:0),p&&p.S?dlt(c.P/(c.S||1),p.P/p.S):null,true);
  // waterfall
  var names=["Revenue"].concat(CO,["Profit"]),base=[],val=[],col=[],run=0;
  names.forEach(function(k,i){
    if(i===0){base.push(0);val.push(c.S);col.push("#a3ddb3");run=c.S;}
    else if(k==="Profit"){base.push(0);val.push(run);col.push(run>=0?"#f5c4af":RED);}
    else{var v=ec[k]||0;run-=v;base.push(Math.max(run,0));val.push(v);col.push(CC[k]);}});
  opt("s-waterfall",{tooltip:{trigger:"axis",axisPointer:{type:"shadow"},formatter:function(a){var x=a[1];return x.name+": "+f2(x.value);}},grid:{left:48,right:12,top:20,bottom:60},
    xAxis:{type:"category",data:names,axisLabel:{color:"#475467",rotate:30,fontSize:10},axisLine:AX.axisLine,axisTick:AX.axisTick},yAxis:yval(),
    series:[{type:"bar",stack:"w",data:base,itemStyle:{color:"transparent"},silent:true},{type:"bar",stack:"w",data:val.map(function(v,i){return {value:Math.round(v),itemStyle:{color:col[i]}};}),label:{show:true,position:"top",formatter:function(q){return kk(q.value);},fontSize:10}}]});
  donut("s-expdonut",CO.filter(function(k){return ec[k];}).map(function(k){return {name:k,value:+ec[k].toFixed(2)};}),usd(c.E),CC);
  var grp=[["Staff (ops + sales)",(ec["Ops staff salary"]||0)+(ec["Sales salary"]||0),"#0e4a7a"],["Direct cost",ec["Direct cost"]||0,"#161616"],["Promo cost",ec["Promo cost"]||0,OR],["Garage & yard",ec["Garage & yard"]||0,"#7a7a7a"],["Back office",ec["Back office"]||0,"#19a803"],["Damage & loss",ec["Damage & loss"]||0,"#e4572e"],["Marketing",ec.Marketing||0,"#bdbdbd"],["Office",ec.Office||0,"#f2c94c"]].sort(function(a,b){return a[1]-b[1];});
  opt("s-expdetail",{tooltip:{valueFormatter:f2},grid:{left:110,right:90,top:10,bottom:20},xAxis:yval(),yAxis:{type:"category",data:grp.map(function(r){return r[0];}),axisLabel:{color:"#475467"},axisLine:AX.axisLine,axisTick:AX.axisTick},
    series:[{type:"bar",data:grp.map(function(r){return {value:Math.round(r[1]),itemStyle:{color:r[2]}};}),label:{show:true,position:"right",formatter:function(q){return usd(q.value)+" ("+(q.value/(c.E||1)*100).toFixed(0)+"%)";}}}]});
  var from=Math.max(1,m-5),cats=[];for(var i=from;i<=m;i++)cats.push(MN[i-1]);
  stacked("s-expbr",cats,CO.map(function(k){var a=[];for(var i=from;i<=m;i++)a.push(Math.round(EC[i][k]||0));return [k,a];}),CO.map(function(k){return CC[k];}));
  $("s-lm").textContent="LAST MONTH · "+(m>1?MN[m-2]:"-");$("s-tm").textContent="THIS MONTH · "+MN[m-1];
  $("s-lmtbl").innerHTML=p?tbl([{t:"Day"},{t:"Profit",bar:"#6f95b3",f:f2}],p.p.map(function(v,i){return {v:[i+1,v]};})):"<p>No previous month.</p>";
  $("s-tmtbl").innerHTML=tbl([{t:"Day"},{t:"Profit",bar:"#6f95b3",f:f2},{t:"vs SPLM",bar:"#7fd18b",f:function(v){return '<span class="'+(v>=0?"up":"down")+'">'+f2(v)+"</span>";}}],
    c.p.map(function(v,i){return {v:[i+1,v,p&&p.p[i]!==undefined?v-p.p[i]:0]};}));
  var li=[],fixed=(ec["Ops staff salary"]||0)+(ec["Sales salary"]||0)+(ec["Garage & yard"]||0)+(ec["Back office"]||0),var_=(ec["Direct cost"]||0)+(ec["Promo cost"]||0)+(ec["Damage & loss"]||0);
  li.push("Direct cost takes <b>"+pc((ec["Direct cost"]||0)/(c.S||1))+"</b> of revenue and staff <b>"+pc(((ec["Ops staff salary"]||0)+(ec["Sales salary"]||0))/(c.S||1))+"</b>: these two lines decide the margin.");
  li.push("Mostly fixed costs (staff, garage, back office) are <b>"+usd(fixed)+"</b>; volume-driven costs (direct, promo, damage) are <b>"+usd(var_)+"</b>. Revenue per day needed to break even on fixed cost alone: <b>"+usd(fixed/dim(m)/(1-(var_/(c.S||1))))+"</b>.");
  var vs=c.p.map(function(v,i){return p?v-(p.p[i]||0):0;}),bi=vs.indexOf(Math.max.apply(null,vs)),wi=vs.indexOf(Math.min.apply(null,vs));
  if(p)li.push("Largest gain vs same day last month: <b>"+MN[m-1]+" "+(bi+1)+"</b> ("+usd(vs[bi])+"); largest drop: <b>"+MN[m-1]+" "+(wi+1)+"</b> ("+usd(vs[wi])+"). Check the weekday and promotions on those days.");
  $("s-pins").innerHTML=ul(li);
  opt("s-splm",{tooltip:{trigger:"axis",valueFormatter:f2},legend:{top:0},color:[INK,"#326a96",GREEN],grid:GR,xAxis:xcat(dd),yAxis:yval(),
    series:[{name:"Profit",type:"line",smooth:true,data:c.p.map(Math.round)},{name:"Profit SPLM",type:"line",smooth:true,data:p?p.p.map(Math.round):[],lineStyle:{type:"dashed"}},
      {name:"vs profit SPLM",type:"bar",data:c.p.map(function(v,i){var d=v-(p?p.p[i]||0:0);return {value:Math.round(d),itemStyle:{color:d>=0?GREEN:RED}};})}]});
}

/* ---------- 6 TEAM ---------- */
function team(m){
  var st=G.staff,cur=st.filter(function(r){return r[0]===m;}),prv=st.filter(function(r){return r[0]===m-1;}),pm={};prv.forEach(function(r){pm[r[1]]=r[2];});
  var tot=sum(cur.map(function(r){return r[2];})),totp=sum(prv.map(function(r){return r[2];})),sal=sum(cur.map(function(r){return r[4]+r[5]+r[6];})),hit=cur.filter(function(r){return r[2]>=r[3];}).length;
  $("s-tkpis").innerHTML=kpi(3,"Rental sales made by team",usd(tot),m>1?dlt(tot,totp):null,true)+kpi(3,"Staff reaching KPI",hit+" / "+cur.length)+kpi(3,"Total sales salary",usd(sal))+kpi(3,"Salary as % of sales made",pc(tot?sal/tot:0));
  var names=cur.map(function(r){return r[1];});
  opt("s-tchart",{tooltip:{trigger:"axis",valueFormatter:f2},legend:{top:0},color:["#9aa3b5",OR],grid:GR,xAxis:xcat(names),yAxis:yval(),
    series:[{name:m>1?"Made "+MN[m-2]:"Previous",type:"bar",data:cur.map(function(r){return Math.round(pm[r[1]]||0);})},
      {name:"Made "+MN[m-1],type:"bar",data:cur.map(function(r){return Math.round(r[2]);}),markLine:{symbol:"none",data:[{yAxis:cur[0]?cur[0][3]:0}],label:{formatter:"KPI target"},lineStyle:{color:INK,type:"dashed"}}}]});
  $("s-ttable").innerHTML=tbl([{t:"Staff"},{t:"Total made",bar:OR,f:f2},{t:"% vs LM",f:function(v){return v==null?"-":'<span class="'+(v>=0?"up":"down")+'">'+(v>=0?"▲ ":"▼ ")+Math.abs(v*100).toFixed(1)+"%</span>";}},{t:"KPI %",f:function(v){return (v*100).toFixed(0)+"%";}},{t:"Commission",f:f2},{t:"Bonus",f:f2},{t:"Total salary",f:f2}],
    cur.map(function(r){return {v:[r[1],r[2],pm[r[1]]?dlt(r[2],pm[r[1]]):null,r[2]/r[3],r[5],r[6],r[4]+r[5]+r[6]]};}));
}

B.pages["s-over"]=over;B.pages["s-sales"]=sales;B.pages["s-promo"]=promo;B.pages["s-cust"]=cust;B.pages["s-profit"]=profit;B.pages["s-team"]=team;
})();
