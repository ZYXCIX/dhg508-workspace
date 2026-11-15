import{g as ce,s as le,p as ue,o as de,a as fe,b as he,_ as l,c as at,d as me,l as st,j as ke,n as ye,q as ge,x as pe}from"./index-B4LVDPE6.js";import{ad as ve,d as kt,F as W}from"./index-CxSLUdi8.js";import{t as Te,m as xe,a as be,i as we,b as _e,c as Nt,d as Bt,e as De,f as Ce,g as Se,h as Ee,j as Ie,k as Me,l as Ae,n as zt,o as jt,p as qt,s as Ht,q as Xt,r as Fe,u as Le,v as $e,w as Oe}from"./advancedFormat-BNio-7k1.js";import{l as Ye}from"./linear-Db8Q23Gm.js";import"./line-BUWQknwM.js";import"./array-BKyUJesY.js";import"./path-CbwjOpE9.js";import"./union-Cn5BbWqs.js";import"./init-Gi6I4Gst.js";import"./defaultLocale-C4B-KCzX.js";var yt={exports:{}},Ve=yt.exports,Ut;function Re(){return Ut||(Ut=1,(function(t,i){(function(r,e){t.exports=e()})(Ve,(function(){var r,e,a=1e3,y=6e4,T=36e5,S=864e5,O=31536e6,z=2628e6,F=/^(-|\+)?P(?:([-+]?[0-9,.]*)Y)?(?:([-+]?[0-9,.]*)M)?(?:([-+]?[0-9,.]*)W)?(?:([-+]?[0-9,.]*)D)?(?:T(?:([-+]?[0-9,.]*)H)?(?:([-+]?[0-9,.]*)M)?(?:([-+]?[0-9,.]*)S)?)?$/,H=/\[([^\]]+)]|YYYY|YY|Y|M{1,2}|D{1,2}|H{1,2}|m{1,2}|s{1,2}|SSS/g,$={years:O,months:z,days:S,hours:T,minutes:y,seconds:a,milliseconds:1,weeks:6048e5},P=function(E){return E instanceof Z},N=function(E,v,m){return new Z(E,m,v.$l)},V=function(E){return e.p(E)+"s"},C=function(E){return E<0},j=function(E){return C(E)?Math.ceil(E):Math.floor(E)},tt=function(E){return Math.abs(E)},X=function(E,v){return E?C(E)?{negative:!0,format:""+tt(E)+v}:{negative:!1,format:""+E+v}:{negative:!1,format:""}},Z=(function(){function E(m,I,h){var g=this;if(this.$d={},this.$l=h,m===void 0&&(this.$ms=0,this.parseFromMilliseconds()),I)return N(m*$[V(I)],this);if(typeof m=="number")return this.$ms=m,this.parseFromMilliseconds(),this;if(typeof m=="object")return Object.keys(m).forEach((function(n){g.$d[V(n)]=m[n]})),this.calMilliseconds(),this;if(typeof m=="string"){var p=m.match(F);if(p){var k=p.slice(2).map((function(n){return n!=null?Number(n):0}));return this.$d.years=k[0],this.$d.months=k[1],this.$d.weeks=k[2],this.$d.days=k[3],this.$d.hours=k[4],this.$d.minutes=k[5],this.$d.seconds=k[6],this.calMilliseconds(),this}}return this}var v=E.prototype;return v.calMilliseconds=function(){var m=this;this.$ms=Object.keys(this.$d).reduce((function(I,h){return I+(m.$d[h]||0)*$[h]}),0)},v.parseFromMilliseconds=function(){var m=this.$ms;this.$d.years=j(m/O),m%=O,this.$d.months=j(m/z),m%=z,this.$d.days=j(m/S),m%=S,this.$d.hours=j(m/T),m%=T,this.$d.minutes=j(m/y),m%=y,this.$d.seconds=j(m/a),m%=a,this.$d.milliseconds=m},v.toISOString=function(){var m=X(this.$d.years,"Y"),I=X(this.$d.months,"M"),h=+this.$d.days||0;this.$d.weeks&&(h+=7*this.$d.weeks);var g=X(h,"D"),p=X(this.$d.hours,"H"),k=X(this.$d.minutes,"M"),n=this.$d.seconds||0;this.$d.milliseconds&&(n+=this.$d.milliseconds/1e3,n=Math.round(1e3*n)/1e3);var d=X(n,"S"),f=m.negative||I.negative||g.negative||p.negative||k.negative||d.negative,u=p.format||k.format||d.format?"T":"",_=(f?"-":"")+"P"+m.format+I.format+g.format+u+p.format+k.format+d.format;return _==="P"||_==="-P"?"P0D":_},v.toJSON=function(){return this.toISOString()},v.format=function(m){var I=m||"YYYY-MM-DDTHH:mm:ss",h={Y:this.$d.years,YY:e.s(this.$d.years,2,"0"),YYYY:e.s(this.$d.years,4,"0"),M:this.$d.months,MM:e.s(this.$d.months,2,"0"),D:this.$d.days,DD:e.s(this.$d.days,2,"0"),H:this.$d.hours,HH:e.s(this.$d.hours,2,"0"),m:this.$d.minutes,mm:e.s(this.$d.minutes,2,"0"),s:this.$d.seconds,ss:e.s(this.$d.seconds,2,"0"),SSS:e.s(this.$d.milliseconds,3,"0")};return I.replace(H,(function(g,p){return p||String(h[g])}))},v.as=function(m){return this.$ms/$[V(m)]},v.get=function(m){var I=this.$ms,h=V(m);return h==="milliseconds"?I%=1e3:I=h==="weeks"?j(I/$[h]):this.$d[h],I||0},v.add=function(m,I,h){var g;return g=I?m*$[V(I)]:P(m)?m.$ms:N(m,this).$ms,N(this.$ms+g*(h?-1:1),this)},v.subtract=function(m,I){return this.add(m,I,!0)},v.locale=function(m){var I=this.clone();return I.$l=m,I},v.clone=function(){return N(this.$ms,this)},v.humanize=function(m){return r().add(this.$ms,"ms").locale(this.$l).fromNow(!m)},v.valueOf=function(){return this.asMilliseconds()},v.milliseconds=function(){return this.get("milliseconds")},v.asMilliseconds=function(){return this.as("milliseconds")},v.seconds=function(){return this.get("seconds")},v.asSeconds=function(){return this.as("seconds")},v.minutes=function(){return this.get("minutes")},v.asMinutes=function(){return this.as("minutes")},v.hours=function(){return this.get("hours")},v.asHours=function(){return this.as("hours")},v.days=function(){return this.get("days")},v.asDays=function(){return this.as("days")},v.weeks=function(){return this.get("weeks")},v.asWeeks=function(){return this.as("weeks")},v.months=function(){return this.get("months")},v.asMonths=function(){return this.as("months")},v.years=function(){return this.get("years")},v.asYears=function(){return this.as("years")},E})(),K=function(E,v,m){return E.add(v.years()*m,"y").add(v.months()*m,"M").add(v.days()*m,"d").add(v.hours()*m,"h").add(v.minutes()*m,"m").add(v.seconds()*m,"s").add(v.milliseconds()*m,"ms")};return function(E,v,m){r=m,e=m().$utils(),m.duration=function(g,p){var k=m.locale();return N(g,{$l:k},p)},m.isDuration=P;var I=v.prototype.add,h=v.prototype.subtract;v.prototype.add=function(g,p){return P(g)?K(this,g,1):I.bind(this)(g,p)},v.prototype.subtract=function(g,p){return P(g)?K(this,g,-1):h.bind(this)(g,p)}}}))})(yt)),yt.exports}var We=Re();const Pe=ve(We);var Dt=(function(){var t=l(function(k,n,d,f){for(d=d||{},f=k.length;f--;d[k[f]]=n);return d},"o"),i=[6,8,10,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31,33,35,36,38,40],r=[1,26],e=[1,27],a=[1,28],y=[1,29],T=[1,30],S=[1,31],O=[1,32],z=[1,33],F=[1,34],H=[1,9],$=[1,10],P=[1,11],N=[1,12],V=[1,13],C=[1,14],j=[1,15],tt=[1,16],X=[1,19],Z=[1,20],K=[1,21],E=[1,22],v=[1,23],m=[1,25],I=[1,35],h={trace:l(function(){},"trace"),yy:{},symbols_:{error:2,start:3,gantt:4,document:5,EOF:6,line:7,SPACE:8,statement:9,NL:10,weekday:11,weekday_monday:12,weekday_tuesday:13,weekday_wednesday:14,weekday_thursday:15,weekday_friday:16,weekday_saturday:17,weekday_sunday:18,weekend:19,weekend_friday:20,weekend_saturday:21,dateFormat:22,inclusiveEndDates:23,topAxis:24,axisFormat:25,tickInterval:26,excludes:27,includes:28,todayMarker:29,title:30,acc_title:31,acc_title_value:32,acc_descr:33,acc_descr_value:34,acc_descr_multiline_value:35,section:36,clickStatement:37,taskTxt:38,taskData:39,click:40,callbackname:41,callbackargs:42,href:43,clickStatementDebug:44,$accept:0,$end:1},terminals_:{2:"error",4:"gantt",6:"EOF",8:"SPACE",10:"NL",12:"weekday_monday",13:"weekday_tuesday",14:"weekday_wednesday",15:"weekday_thursday",16:"weekday_friday",17:"weekday_saturday",18:"weekday_sunday",20:"weekend_friday",21:"weekend_saturday",22:"dateFormat",23:"inclusiveEndDates",24:"topAxis",25:"axisFormat",26:"tickInterval",27:"excludes",28:"includes",29:"todayMarker",30:"title",31:"acc_title",32:"acc_title_value",33:"acc_descr",34:"acc_descr_value",35:"acc_descr_multiline_value",36:"section",38:"taskTxt",39:"taskData",40:"click",41:"callbackname",42:"callbackargs",43:"href"},productions_:[0,[3,3],[5,0],[5,2],[7,2],[7,1],[7,1],[7,1],[11,1],[11,1],[11,1],[11,1],[11,1],[11,1],[11,1],[19,1],[19,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,2],[9,2],[9,1],[9,1],[9,1],[9,2],[37,2],[37,3],[37,3],[37,4],[37,3],[37,4],[37,2],[44,2],[44,3],[44,3],[44,4],[44,3],[44,4],[44,2]],performAction:l(function(n,d,f,u,_,s,D){var c=s.length-1;switch(_){case 1:return s[c-1];case 2:this.$=[];break;case 3:s[c-1].push(s[c]),this.$=s[c-1];break;case 4:case 5:this.$=s[c];break;case 6:case 7:this.$=[];break;case 8:u.setWeekday("monday");break;case 9:u.setWeekday("tuesday");break;case 10:u.setWeekday("wednesday");break;case 11:u.setWeekday("thursday");break;case 12:u.setWeekday("friday");break;case 13:u.setWeekday("saturday");break;case 14:u.setWeekday("sunday");break;case 15:u.setWeekend("friday");break;case 16:u.setWeekend("saturday");break;case 17:u.setDateFormat(s[c].substr(11)),this.$=s[c].substr(11);break;case 18:u.enableInclusiveEndDates(),this.$=s[c].substr(18);break;case 19:u.TopAxis(),this.$=s[c].substr(8);break;case 20:u.setAxisFormat(s[c].substr(11)),this.$=s[c].substr(11);break;case 21:u.setTickInterval(s[c].substr(13)),this.$=s[c].substr(13);break;case 22:u.setExcludes(s[c].substr(9)),this.$=s[c].substr(9);break;case 23:u.setIncludes(s[c].substr(9)),this.$=s[c].substr(9);break;case 24:u.setTodayMarker(s[c].substr(12)),this.$=s[c].substr(12);break;case 27:u.setDiagramTitle(s[c].substr(6)),this.$=s[c].substr(6);break;case 28:this.$=s[c].trim(),u.setAccTitle(this.$);break;case 29:case 30:this.$=s[c].trim(),u.setAccDescription(this.$);break;case 31:u.addSection(s[c].substr(8)),this.$=s[c].substr(8);break;case 33:u.addTask(s[c-1],s[c]),this.$="task";break;case 34:this.$=s[c-1],u.setClickEvent(s[c-1],s[c],null);break;case 35:this.$=s[c-2],u.setClickEvent(s[c-2],s[c-1],s[c]);break;case 36:this.$=s[c-2],u.setClickEvent(s[c-2],s[c-1],null),u.setLink(s[c-2],s[c]);break;case 37:this.$=s[c-3],u.setClickEvent(s[c-3],s[c-2],s[c-1]),u.setLink(s[c-3],s[c]);break;case 38:this.$=s[c-2],u.setClickEvent(s[c-2],s[c],null),u.setLink(s[c-2],s[c-1]);break;case 39:this.$=s[c-3],u.setClickEvent(s[c-3],s[c-1],s[c]),u.setLink(s[c-3],s[c-2]);break;case 40:this.$=s[c-1],u.setLink(s[c-1],s[c]);break;case 41:case 47:this.$=s[c-1]+" "+s[c];break;case 42:case 43:case 45:this.$=s[c-2]+" "+s[c-1]+" "+s[c];break;case 44:case 46:this.$=s[c-3]+" "+s[c-2]+" "+s[c-1]+" "+s[c];break}},"anonymous"),table:[{3:1,4:[1,2]},{1:[3]},t(i,[2,2],{5:3}),{6:[1,4],7:5,8:[1,6],9:7,10:[1,8],11:17,12:r,13:e,14:a,15:y,16:T,17:S,18:O,19:18,20:z,21:F,22:H,23:$,24:P,25:N,26:V,27:C,28:j,29:tt,30:X,31:Z,33:K,35:E,36:v,37:24,38:m,40:I},t(i,[2,7],{1:[2,1]}),t(i,[2,3]),{9:36,11:17,12:r,13:e,14:a,15:y,16:T,17:S,18:O,19:18,20:z,21:F,22:H,23:$,24:P,25:N,26:V,27:C,28:j,29:tt,30:X,31:Z,33:K,35:E,36:v,37:24,38:m,40:I},t(i,[2,5]),t(i,[2,6]),t(i,[2,17]),t(i,[2,18]),t(i,[2,19]),t(i,[2,20]),t(i,[2,21]),t(i,[2,22]),t(i,[2,23]),t(i,[2,24]),t(i,[2,25]),t(i,[2,26]),t(i,[2,27]),{32:[1,37]},{34:[1,38]},t(i,[2,30]),t(i,[2,31]),t(i,[2,32]),{39:[1,39]},t(i,[2,8]),t(i,[2,9]),t(i,[2,10]),t(i,[2,11]),t(i,[2,12]),t(i,[2,13]),t(i,[2,14]),t(i,[2,15]),t(i,[2,16]),{41:[1,40],43:[1,41]},t(i,[2,4]),t(i,[2,28]),t(i,[2,29]),t(i,[2,33]),t(i,[2,34],{42:[1,42],43:[1,43]}),t(i,[2,40],{41:[1,44]}),t(i,[2,35],{43:[1,45]}),t(i,[2,36]),t(i,[2,38],{42:[1,46]}),t(i,[2,37]),t(i,[2,39])],defaultActions:{},parseError:l(function(n,d){if(d.recoverable)this.trace(n);else{var f=new Error(n);throw f.hash=d,f}},"parseError"),parse:l(function(n){var d=this,f=[0],u=[],_=[null],s=[],D=this.table,c="",R=0,o=0,x=2,b=1,M=s.slice.call(arguments,1),w=Object.create(this.lexer),L={yy:{}};for(var A in this.yy)Object.prototype.hasOwnProperty.call(this.yy,A)&&(L.yy[A]=this.yy[A]);w.setInput(n,L.yy),L.yy.lexer=w,L.yy.parser=this,typeof w.yylloc>"u"&&(w.yylloc={});var dt=w.yylloc;s.push(dt);var xt=w.options&&w.options.ranges;typeof L.yy.parseError=="function"?this.parseError=L.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;function oe(q){f.length=f.length-2*q,_.length=_.length-q,s.length=s.length-q}l(oe,"popStack");function Wt(){var q;return q=u.pop()||w.lex()||b,typeof q!="number"&&(q instanceof Array&&(u=q,q=u.pop()),q=d.symbols_[q]||q),q}l(Wt,"lex");for(var B,et,U,bt,rt={},ht,J,Pt,mt;;){if(et=f[f.length-1],this.defaultActions[et]?U=this.defaultActions[et]:((B===null||typeof B>"u")&&(B=Wt()),U=D[et]&&D[et][B]),typeof U>"u"||!U.length||!U[0]){var wt="";mt=[];for(ht in D[et])this.terminals_[ht]&&ht>x&&mt.push("'"+this.terminals_[ht]+"'");w.showPosition?wt="Parse error on line "+(R+1)+`:
`+w.showPosition()+`
Expecting `+mt.join(", ")+", got '"+(this.terminals_[B]||B)+"'":wt="Parse error on line "+(R+1)+": Unexpected "+(B==b?"end of input":"'"+(this.terminals_[B]||B)+"'"),this.parseError(wt,{text:w.match,token:this.terminals_[B]||B,line:w.yylineno,loc:dt,expected:mt})}if(U[0]instanceof Array&&U.length>1)throw new Error("Parse Error: multiple actions possible at state: "+et+", token: "+B);switch(U[0]){case 1:f.push(B),_.push(w.yytext),s.push(w.yylloc),f.push(U[1]),B=null,o=w.yyleng,c=w.yytext,R=w.yylineno,dt=w.yylloc;break;case 2:if(J=this.productions_[U[1]][1],rt.$=_[_.length-J],rt._$={first_line:s[s.length-(J||1)].first_line,last_line:s[s.length-1].last_line,first_column:s[s.length-(J||1)].first_column,last_column:s[s.length-1].last_column},xt&&(rt._$.range=[s[s.length-(J||1)].range[0],s[s.length-1].range[1]]),bt=this.performAction.apply(rt,[c,o,R,L.yy,U[1],_,s].concat(M)),typeof bt<"u")return bt;J&&(f=f.slice(0,-1*J*2),_=_.slice(0,-1*J),s=s.slice(0,-1*J)),f.push(this.productions_[U[1]][0]),_.push(rt.$),s.push(rt._$),Pt=D[f[f.length-2]][f[f.length-1]],f.push(Pt);break;case 3:return!0}}return!0},"parse")},g=(function(){var k={EOF:1,parseError:l(function(d,f){if(this.yy.parser)this.yy.parser.parseError(d,f);else throw new Error(d)},"parseError"),setInput:l(function(n,d){return this.yy=d||this.yy||{},this._input=n,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},"setInput"),input:l(function(){var n=this._input[0];this.yytext+=n,this.yyleng++,this.offset++,this.match+=n,this.matched+=n;var d=n.match(/(?:\r\n?|\n).*/g);return d?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),n},"input"),unput:l(function(n){var d=n.length,f=n.split(/(?:\r\n?|\n)/g);this._input=n+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-d),this.offset-=d;var u=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),f.length-1&&(this.yylineno-=f.length-1);var _=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:f?(f.length===u.length?this.yylloc.first_column:0)+u[u.length-f.length].length-f[0].length:this.yylloc.first_column-d},this.options.ranges&&(this.yylloc.range=[_[0],_[0]+this.yyleng-d]),this.yyleng=this.yytext.length,this},"unput"),more:l(function(){return this._more=!0,this},"more"),reject:l(function(){if(this.options.backtrack_lexer)this._backtrack=!0;else return this.parseError("Lexical error on line "+(this.yylineno+1)+`. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
`+this.showPosition(),{text:"",token:null,line:this.yylineno});return this},"reject"),less:l(function(n){this.unput(this.match.slice(n))},"less"),pastInput:l(function(){var n=this.matched.substr(0,this.matched.length-this.match.length);return(n.length>20?"...":"")+n.substr(-20).replace(/\n/g,"")},"pastInput"),upcomingInput:l(function(){var n=this.match;return n.length<20&&(n+=this._input.substr(0,20-n.length)),(n.substr(0,20)+(n.length>20?"...":"")).replace(/\n/g,"")},"upcomingInput"),showPosition:l(function(){var n=this.pastInput(),d=new Array(n.length+1).join("-");return n+this.upcomingInput()+`
`+d+"^"},"showPosition"),test_match:l(function(n,d){var f,u,_;if(this.options.backtrack_lexer&&(_={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(_.yylloc.range=this.yylloc.range.slice(0))),u=n[0].match(/(?:\r\n?|\n).*/g),u&&(this.yylineno+=u.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:u?u[u.length-1].length-u[u.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+n[0].length},this.yytext+=n[0],this.match+=n[0],this.matches=n,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(n[0].length),this.matched+=n[0],f=this.performAction.call(this,this.yy,this,d,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),f)return f;if(this._backtrack){for(var s in _)this[s]=_[s];return!1}return!1},"test_match"),next:l(function(){if(this.done)return this.EOF;this._input||(this.done=!0);var n,d,f,u;this._more||(this.yytext="",this.match="");for(var _=this._currentRules(),s=0;s<_.length;s++)if(f=this._input.match(this.rules[_[s]]),f&&(!d||f[0].length>d[0].length)){if(d=f,u=s,this.options.backtrack_lexer){if(n=this.test_match(f,_[s]),n!==!1)return n;if(this._backtrack){d=!1;continue}else return!1}else if(!this.options.flex)break}return d?(n=this.test_match(d,_[u]),n!==!1?n:!1):this._input===""?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+`. Unrecognized text.
`+this.showPosition(),{text:"",token:null,line:this.yylineno})},"next"),lex:l(function(){var d=this.next();return d||this.lex()},"lex"),begin:l(function(d){this.conditionStack.push(d)},"begin"),popState:l(function(){var d=this.conditionStack.length-1;return d>0?this.conditionStack.pop():this.conditionStack[0]},"popState"),_currentRules:l(function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},"_currentRules"),topState:l(function(d){return d=this.conditionStack.length-1-Math.abs(d||0),d>=0?this.conditionStack[d]:"INITIAL"},"topState"),pushState:l(function(d){this.begin(d)},"pushState"),stateStackSize:l(function(){return this.conditionStack.length},"stateStackSize"),options:{"case-insensitive":!0},performAction:l(function(d,f,u,_){switch(u){case 0:return this.begin("open_directive"),"open_directive";case 1:return this.begin("acc_title"),31;case 2:return this.popState(),"acc_title_value";case 3:return this.begin("acc_descr"),33;case 4:return this.popState(),"acc_descr_value";case 5:this.begin("acc_descr_multiline");break;case 6:this.popState();break;case 7:return"acc_descr_multiline_value";case 8:break;case 9:break;case 10:break;case 11:return 10;case 12:break;case 13:break;case 14:this.begin("href");break;case 15:this.popState();break;case 16:return 43;case 17:this.begin("callbackname");break;case 18:this.popState();break;case 19:this.popState(),this.begin("callbackargs");break;case 20:return 41;case 21:this.popState();break;case 22:return 42;case 23:this.begin("click");break;case 24:this.popState();break;case 25:return 40;case 26:return 4;case 27:return 22;case 28:return 23;case 29:return 24;case 30:return 25;case 31:return 26;case 32:return 28;case 33:return 27;case 34:return 29;case 35:return 12;case 36:return 13;case 37:return 14;case 38:return 15;case 39:return 16;case 40:return 17;case 41:return 18;case 42:return 20;case 43:return 21;case 44:return"date";case 45:return 30;case 46:return"accDescription";case 47:return 36;case 48:return 38;case 49:return 39;case 50:return":";case 51:return 6;case 52:return"INVALID"}},"anonymous"),rules:[/^(?:%%\{)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:%%(?!\{)*[^\n]*)/i,/^(?:[^\}]%%*[^\n]*)/i,/^(?:%%*[^\n]*[\n]*)/i,/^(?:[\n]+)/i,/^(?:\s+)/i,/^(?:%[^\n]*)/i,/^(?:href[\s]+["])/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:call[\s]+)/i,/^(?:\([\s]*\))/i,/^(?:\()/i,/^(?:[^(]*)/i,/^(?:\))/i,/^(?:[^)]*)/i,/^(?:click[\s]+)/i,/^(?:[\s\n])/i,/^(?:[^\s\n]*)/i,/^(?:gantt\b)/i,/^(?:dateFormat\s[^#\n;]+)/i,/^(?:inclusiveEndDates\b)/i,/^(?:topAxis\b)/i,/^(?:axisFormat\s[^#\n;]+)/i,/^(?:tickInterval\s[^#\n;]+)/i,/^(?:includes\s[^#\n;]+)/i,/^(?:excludes\s[^#\n;]+)/i,/^(?:todayMarker\s[^\n;]+)/i,/^(?:weekday\s+monday\b)/i,/^(?:weekday\s+tuesday\b)/i,/^(?:weekday\s+wednesday\b)/i,/^(?:weekday\s+thursday\b)/i,/^(?:weekday\s+friday\b)/i,/^(?:weekday\s+saturday\b)/i,/^(?:weekday\s+sunday\b)/i,/^(?:weekend\s+friday\b)/i,/^(?:weekend\s+saturday\b)/i,/^(?:\d\d\d\d-\d\d-\d\d\b)/i,/^(?:title\s[^\n]+)/i,/^(?:accDescription\s[^#\n;]+)/i,/^(?:section\s[^\n]+)/i,/^(?:[^:\n]+)/i,/^(?::[^#\n;]+)/i,/^(?::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{acc_descr_multiline:{rules:[6,7],inclusive:!1},acc_descr:{rules:[4],inclusive:!1},acc_title:{rules:[2],inclusive:!1},callbackargs:{rules:[21,22],inclusive:!1},callbackname:{rules:[18,19,20],inclusive:!1},href:{rules:[15,16],inclusive:!1},click:{rules:[24,25],inclusive:!1},INITIAL:{rules:[0,1,3,5,8,9,10,11,12,13,14,17,23,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52],inclusive:!0}}};return k})();h.lexer=g;function p(){this.yy={}}return l(p,"Parser"),p.prototype=h,h.Parser=p,new p})();Dt.parser=Dt;var Ne=Dt;W.extend(Le);W.extend($e);W.extend(Oe);var Gt={friday:5,saturday:6},G="",It="",Mt=void 0,At="",ct=[],lt=[],Ft=new Map,Lt=[],vt=[],ut="",$t="",Qt=["active","done","crit","milestone","vert"],Ot=[],nt="",ft=!1,Yt=!1,Vt="sunday",Tt="saturday",Ct=0,Be=l(function(){Lt=[],vt=[],ut="",Ot=[],gt=0,Et=void 0,pt=void 0,Y=[],G="",It="",$t="",Mt=void 0,At="",ct=[],lt=[],ft=!1,Yt=!1,Ct=0,Ft=new Map,nt="",ge(),Vt="sunday",Tt="saturday"},"clear"),ze=l(function(t){nt=t},"setDiagramId"),je=l(function(t){It=t},"setAxisFormat"),qe=l(function(){return It},"getAxisFormat"),He=l(function(t){Mt=t},"setTickInterval"),Xe=l(function(){return Mt},"getTickInterval"),Ue=l(function(t){At=t},"setTodayMarker"),Ge=l(function(){return At},"getTodayMarker"),Ke=l(function(t){G=t},"setDateFormat"),Je=l(function(){ft=!0},"enableInclusiveEndDates"),Qe=l(function(){return ft},"endDatesAreInclusive"),Ze=l(function(){Yt=!0},"enableTopAxis"),ts=l(function(){return Yt},"topAxisEnabled"),es=l(function(t){$t=t},"setDisplayMode"),ss=l(function(){return $t},"getDisplayMode"),is=l(function(){return G},"getDateFormat"),Zt=l((t,i)=>{const r=i.toLowerCase().split(/[\s,]+/).filter(e=>e!=="");return[...new Set([...t,...r])]},"mergeTokens"),rs=l(function(t){ct=Zt(ct,t)},"setIncludes"),ns=l(function(){return ct},"getIncludes"),as=l(function(t){lt=Zt(lt,t)},"setExcludes"),os=l(function(){return lt},"getExcludes"),cs=l(function(){return Ft},"getLinks"),ls=l(function(t){ut=t,Lt.push(t)},"addSection"),us=l(function(){return Lt},"getSections"),ds=l(function(){let t=Kt();const i=10;let r=0;for(;!t&&r<i;)t=Kt(),r++;return vt=Y,vt},"getTasks"),te=l(function(t,i,r,e){const a=t.format(i.trim()),y=t.format("YYYY-MM-DD");return e.includes(a)||e.includes(y)?!1:r.includes("weekends")&&(t.isoWeekday()===Gt[Tt]||t.isoWeekday()===Gt[Tt]+1)||r.includes(t.format("dddd").toLowerCase())?!0:r.includes(a)||r.includes(y)},"isInvalidDate"),fs=l(function(t){Vt=t},"setWeekday"),hs=l(function(){return Vt},"getWeekday"),ms=l(function(t){Tt=t},"setWeekend"),ee=l(function(t,i,r,e){if(!r.length||t.manualEndTime)return;let a;t.startTime instanceof Date?a=W(t.startTime):a=W(t.startTime,i,!0),a=a.add(1,"d");let y;t.endTime instanceof Date?y=W(t.endTime):y=W(t.endTime,i,!0);const[T,S]=ks(a,y,i,r,e);t.endTime=T.toDate(),t.renderEndTime=S},"checkTaskDates"),ks=l(function(t,i,r,e,a){let y=!1,T=null;const S=i.add(1e4,"d");for(;t<=i;){if(y||(T=i.toDate()),y=te(t,r,e,a),y&&(i=i.add(1,"d"),i>S))throw new Error("Failed to find a valid date that was not excluded by `excludes` after 10,000 iterations.");t=t.add(1,"d")}return[i,T]},"fixTaskDates"),St=l(function(t,i,r){if(r=r.trim(),l(S=>{const O=S.trim();return O==="x"||O==="X"},"isTimestampFormat")(i)&&/^\d+$/.test(r))return new Date(Number(r));const y=/^after\s+(?<ids>[\d\w- ]+)/.exec(r);if(y!==null){let S=null;for(const z of y.groups.ids.split(" ")){let F=it(z);F!==void 0&&(!S||F.endTime>S.endTime)&&(S=F)}if(S)return S.endTime;const O=new Date;return O.setHours(0,0,0,0),O}let T=W(r,i.trim(),!0);if(T.isValid())return T.toDate();{st.debug("Invalid date:"+r),st.debug("With date format:"+i.trim());const S=new Date(r);if(S===void 0||isNaN(S.getTime())||S.getFullYear()<-1e4||S.getFullYear()>1e4)throw new Error("Invalid date:"+r);return S}},"getStartDate"),se=l(function(t){const i=/^(\d+(?:\.\d+)?)([Mdhmswy]|ms)$/.exec(t.trim());return i!==null?[Number.parseFloat(i[1]),i[2]]:[NaN,"ms"]},"parseDuration"),ie=l(function(t,i,r,e=!1){r=r.trim();const y=/^until\s+(?<ids>[\d\w- ]+)/.exec(r);if(y!==null){let F=null;for(const $ of y.groups.ids.split(" ")){let P=it($);P!==void 0&&(!F||P.startTime<F.startTime)&&(F=P)}if(F)return F.startTime;const H=new Date;return H.setHours(0,0,0,0),H}let T=W(r,i.trim(),!0);if(T.isValid())return e&&(T=T.add(1,"d")),T.toDate();let S=W(t);const[O,z]=se(r);if(!Number.isNaN(O)){const F=S.add(O,z);F.isValid()&&(S=F)}return S.toDate()},"getEndDate"),gt=0,ot=l(function(t){return t===void 0?(gt=gt+1,"task"+gt):t},"parseId"),ys=l(function(t,i){let r;i.substr(0,1)===":"?r=i.substr(1,i.length):r=i;const e=r.split(","),a={};Rt(e,a,Qt);for(let T=0;T<e.length;T++)e[T]=e[T].trim();let y="";switch(e.length){case 1:a.id=ot(),a.startTime=t.endTime,y=e[0];break;case 2:a.id=ot(),a.startTime=St(void 0,G,e[0]),y=e[1];break;case 3:a.id=ot(e[0]),a.startTime=St(void 0,G,e[1]),y=e[2];break}return y&&(a.endTime=ie(a.startTime,G,y,ft),a.manualEndTime=W(y,"YYYY-MM-DD",!0).isValid(),ee(a,G,lt,ct)),a},"compileData"),gs=l(function(t,i){let r;i.substr(0,1)===":"?r=i.substr(1,i.length):r=i;const e=r.split(","),a={};Rt(e,a,Qt);for(let y=0;y<e.length;y++)e[y]=e[y].trim();switch(e.length){case 1:a.id=ot(),a.startTime={type:"prevTaskEnd",id:t},a.endTime={data:e[0]};break;case 2:a.id=ot(),a.startTime={type:"getStartDate",startData:e[0]},a.endTime={data:e[1]};break;case 3:a.id=ot(e[0]),a.startTime={type:"getStartDate",startData:e[1]},a.endTime={data:e[2]};break}return a},"parseData"),Et,pt,Y=[],re={},ps=l(function(t,i){const r={section:ut,type:ut,processed:!1,manualEndTime:!1,renderEndTime:null,raw:{data:i},task:t,classes:[]},e=gs(pt,i);r.raw.startTime=e.startTime,r.raw.endTime=e.endTime,r.id=e.id,r.prevTaskId=pt,r.active=e.active,r.done=e.done,r.crit=e.crit,r.milestone=e.milestone,r.vert=e.vert,r.vert?r.order=-1:(r.order=Ct,Ct++);const a=Y.push(r);pt=r.id,re[r.id]=a-1},"addTask"),it=l(function(t){const i=re[t];return Y[i]},"findTaskById"),vs=l(function(t,i){const r={section:ut,type:ut,description:t,task:t,classes:[]},e=ys(Et,i);r.startTime=e.startTime,r.endTime=e.endTime,r.id=e.id,r.active=e.active,r.done=e.done,r.crit=e.crit,r.milestone=e.milestone,r.vert=e.vert,Et=r,vt.push(r)},"addTaskOrg"),Kt=l(function(){const t=l(function(r){const e=Y[r];let a="";switch(Y[r].raw.startTime.type){case"prevTaskEnd":{const y=it(e.prevTaskId);e.startTime=y.endTime;break}case"getStartDate":a=St(void 0,G,Y[r].raw.startTime.startData),a&&(Y[r].startTime=a);break}return Y[r].startTime&&(Y[r].endTime=ie(Y[r].startTime,G,Y[r].raw.endTime.data,ft),Y[r].endTime&&(Y[r].processed=!0,Y[r].manualEndTime=W(Y[r].raw.endTime.data,"YYYY-MM-DD",!0).isValid(),ee(Y[r],G,lt,ct))),Y[r].processed},"compileTask");let i=!0;for(const[r,e]of Y.entries())t(r),i=i&&e.processed;return i},"compileTasks"),Ts=l(function(t,i){let r=i;at().securityLevel!=="loose"&&(r=ye.sanitizeUrl(i)),t.split(",").forEach(function(e){it(e)!==void 0&&(ae(e,()=>{window.open(r,"_self")}),Ft.set(e,r))}),ne(t,"clickable")},"setLink"),ne=l(function(t,i){t.split(",").forEach(function(r){let e=it(r);e!==void 0&&e.classes.push(i)})},"setClass"),xs=l(function(t,i,r){if(at().securityLevel!=="loose"||i===void 0)return;let e=[];if(typeof r=="string"){e=r.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);for(let y=0;y<e.length;y++){let T=e[y].trim();T.startsWith('"')&&T.endsWith('"')&&(T=T.substr(1,T.length-2)),e[y]=T}}e.length===0&&e.push(t),it(t)!==void 0&&ae(t,()=>{pe.runFunc(i,...e)})},"setClickFun"),ae=l(function(t,i){Ot.push(function(){const r=nt?`${nt}-${t}`:t,e=document.querySelector(`[id="${r}"]`);e!==null&&e.addEventListener("click",function(){i()})},function(){const r=nt?`${nt}-${t}`:t,e=document.querySelector(`[id="${r}-text"]`);e!==null&&e.addEventListener("click",function(){i()})})},"pushFun"),bs=l(function(t,i,r){t.split(",").forEach(function(e){xs(e,i,r)}),ne(t,"clickable")},"setClickEvent"),ws=l(function(t){Ot.forEach(function(i){i(t)})},"bindFunctions"),_s={getConfig:l(()=>at().gantt,"getConfig"),clear:Be,setDateFormat:Ke,getDateFormat:is,enableInclusiveEndDates:Je,endDatesAreInclusive:Qe,enableTopAxis:Ze,topAxisEnabled:ts,setAxisFormat:je,getAxisFormat:qe,setTickInterval:He,getTickInterval:Xe,setTodayMarker:Ue,getTodayMarker:Ge,setAccTitle:he,getAccTitle:fe,setDiagramTitle:de,getDiagramTitle:ue,setDiagramId:ze,setDisplayMode:es,getDisplayMode:ss,setAccDescription:le,getAccDescription:ce,addSection:ls,getSections:us,getTasks:ds,addTask:ps,findTaskById:it,addTaskOrg:vs,setIncludes:rs,getIncludes:ns,setExcludes:as,getExcludes:os,setClickEvent:bs,setLink:Ts,getLinks:cs,bindFunctions:ws,parseDuration:se,isInvalidDate:te,setWeekday:fs,getWeekday:hs,setWeekend:ms};function Rt(t,i,r){let e=!0;for(;e;)e=!1,r.forEach(function(a){const y="^\\s*"+a+"\\s*$",T=new RegExp(y);t[0].match(T)&&(i[a]=!0,t.shift(1),e=!0)})}l(Rt,"getTaskTags");W.extend(Pe);var Ds=l(function(){st.debug("Something is calling, setConf, remove the call")},"setConf"),Jt={monday:Ae,tuesday:Me,wednesday:Ie,thursday:Ee,friday:Se,saturday:Ce,sunday:De},Cs=l((t,i)=>{let r=[...t].map(()=>-1/0),e=[...t].sort((y,T)=>y.startTime-T.startTime||y.order-T.order),a=0;for(const y of e)for(let T=0;T<r.length;T++)if(y.startTime>=r[T]){r[T]=y.endTime,y.order=T+i,T>a&&(a=T);break}return a},"getMaxIntersections"),Q,_t=1e4,Ss=l(function(t,i,r,e){const a=at().gantt;e.db.setDiagramId(i);const y=at().securityLevel;let T;y==="sandbox"&&(T=kt("#i"+i));const S=y==="sandbox"?kt(T.nodes()[0].contentDocument.body):kt("body"),O=y==="sandbox"?T.nodes()[0].contentDocument:document,z=O.getElementById(i);Q=z.parentElement.offsetWidth,Q===void 0&&(Q=1200),a.useWidth!==void 0&&(Q=a.useWidth);const F=e.db.getTasks(),H=F.filter(h=>!h.vert);let $=[];for(const h of H)$.push(h.type);$=I($);const P={};let N=2*a.topPadding;if(e.db.getDisplayMode()==="compact"||a.displayMode==="compact"){const h={};for(const p of H)h[p.section]===void 0?h[p.section]=[p]:h[p.section].push(p);let g=0;for(const p of Object.keys(h)){const k=Cs(h[p],g)+1;g+=k,N+=k*(a.barHeight+a.barGap),P[p]=k}}else{N+=H.length*(a.barHeight+a.barGap);for(const h of $)P[h]=H.filter(g=>g.type===h).length}z.setAttribute("viewBox","0 0 "+Q+" "+N);const V=S.select(`[id="${i}"]`),C=Te().domain([xe(F,function(h){return h.startTime}),be(F,function(h){return h.endTime})]).rangeRound([0,Q-a.leftPadding-a.rightPadding]);function j(h,g){const p=h.startTime,k=g.startTime;let n=0;return p>k?n=1:p<k&&(n=-1),n}l(j,"taskCompare"),F.sort(j),tt(F,Q,N),me(V,N,Q,a.useMaxWidth),V.append("text").text(e.db.getDiagramTitle()).attr("x",Q/2).attr("y",a.titleTopMargin).attr("class","titleText");function tt(h,g,p){const k=a.barHeight,n=k+a.barGap,d=a.topPadding,f=a.leftPadding,u=Ye().domain([0,$.length]).range(["#00B9FA","#F95002"]).interpolate(we);Z(n,d,f,g,p,h,e.db.getExcludes(),e.db.getIncludes()),E(f,d,g,p),X(h,n,d,f,k,u,g),v(n,d),m(f,d,g,p)}l(tt,"makeGantt");function X(h,g,p,k,n,d,f){h.sort((o,x)=>o.vert===x.vert?0:o.vert?1:-1);const u=h.filter(o=>!o.vert),s=[...new Set(u.map(o=>o.order))].map(o=>u.find(x=>x.order===o));V.append("g").selectAll("rect").data(s).enter().append("rect").attr("x",0).attr("y",function(o,x){return x=o.order,x*g+p-2}).attr("width",function(){return f-a.rightPadding/2}).attr("height",g).attr("class",function(o){for(const[x,b]of $.entries())if(o.type===b)return"section section"+x%a.numberSectionStyles;return"section section0"}).enter();const D=V.append("g").selectAll("rect").data(h).enter(),c=e.db.getLinks();if(D.append("rect").attr("id",function(o){return i+"-"+o.id}).attr("rx",3).attr("ry",3).attr("x",function(o){return o.milestone?C(o.startTime)+k+.5*(C(o.endTime)-C(o.startTime))-.5*n:C(o.startTime)+k}).attr("y",function(o,x){return x=o.order,o.vert?a.gridLineStartPadding:x*g+p}).attr("width",function(o){return o.milestone?n:o.vert?.08*n:C(o.renderEndTime||o.endTime)-C(o.startTime)}).attr("height",function(o){return o.vert?u.length*(a.barHeight+a.barGap)+a.barHeight*2:n}).attr("transform-origin",function(o,x){return x=o.order,(C(o.startTime)+k+.5*(C(o.endTime)-C(o.startTime))).toString()+"px "+(x*g+p+.5*n).toString()+"px"}).attr("class",function(o){const x="task";let b="";o.classes.length>0&&(b=o.classes.join(" "));let M=0;for(const[L,A]of $.entries())o.type===A&&(M=L%a.numberSectionStyles);let w="";return o.active?o.crit?w+=" activeCrit":w=" active":o.done?o.crit?w=" doneCrit":w=" done":o.crit&&(w+=" crit"),w.length===0&&(w=" task"),o.milestone&&(w=" milestone "+w),o.vert&&(w=" vert "+w),w+=M,w+=" "+b,x+w}),D.append("text").attr("id",function(o){return i+"-"+o.id+"-text"}).text(function(o){return o.task}).attr("font-size",a.fontSize).attr("x",function(o){let x=C(o.startTime),b=C(o.renderEndTime||o.endTime);if(o.milestone&&(x+=.5*(C(o.endTime)-C(o.startTime))-.5*n,b=x+n),o.vert)return C(o.startTime)+k;const M=this.getBBox().width;return M>b-x?b+M+1.5*a.leftPadding>f?x+k-5:b+k+5:(b-x)/2+x+k}).attr("y",function(o,x){return o.vert?a.gridLineStartPadding+u.length*(a.barHeight+a.barGap)+60:(x=o.order,x*g+a.barHeight/2+(a.fontSize/2-2)+p)}).attr("text-height",n).attr("class",function(o){const x=C(o.startTime);let b=C(o.endTime);o.milestone&&(b=x+n);const M=this.getBBox().width;let w="";o.classes.length>0&&(w=o.classes.join(" "));let L=0;for(const[dt,xt]of $.entries())o.type===xt&&(L=dt%a.numberSectionStyles);let A="";return o.active&&(o.crit?A="activeCritText"+L:A="activeText"+L),o.done?o.crit?A=A+" doneCritText"+L:A=A+" doneText"+L:o.crit&&(A=A+" critText"+L),o.milestone&&(A+=" milestoneText"),o.vert&&(A+=" vertText"),M>b-x?b+M+1.5*a.leftPadding>f?w+" taskTextOutsideLeft taskTextOutside"+L+" "+A:w+" taskTextOutsideRight taskTextOutside"+L+" "+A+" width-"+M:w+" taskText taskText"+L+" "+A+" width-"+M}),at().securityLevel==="sandbox"){let o;o=kt("#i"+i);const x=o.nodes()[0].contentDocument;D.filter(function(b){return c.has(b.id)}).each(function(b){var M=x.querySelector("#"+CSS.escape(i+"-"+b.id)),w=x.querySelector("#"+CSS.escape(i+"-"+b.id+"-text"));const L=M.parentNode;var A=x.createElement("a");A.setAttribute("xlink:href",c.get(b.id)),A.setAttribute("target","_top"),L.appendChild(A),A.appendChild(M),A.appendChild(w)})}}l(X,"drawRects");function Z(h,g,p,k,n,d,f,u){if(f.length===0&&u.length===0)return;let _,s;for(const{startTime:b,endTime:M}of d)(_===void 0||b<_)&&(_=b),(s===void 0||M>s)&&(s=M);if(!_||!s)return;if(W(s).diff(W(_),"year")>5){st.warn("The difference between the min and max time is more than 5 years. This will cause performance issues. Skipping drawing exclude days.");return}const D=e.db.getDateFormat(),c=[];let R=null,o=W(_);for(;o.valueOf()<=s;)e.db.isInvalidDate(o,D,f,u)?R?R.end=o:R={start:o,end:o}:R&&(c.push(R),R=null),o=o.add(1,"d");V.append("g").selectAll("rect").data(c).enter().append("rect").attr("id",b=>i+"-exclude-"+b.start.format("YYYY-MM-DD")).attr("x",b=>C(b.start.startOf("day"))+p).attr("y",a.gridLineStartPadding).attr("width",b=>C(b.end.endOf("day"))-C(b.start.startOf("day"))).attr("height",n-g-a.gridLineStartPadding).attr("transform-origin",function(b,M){return(C(b.start)+p+.5*(C(b.end)-C(b.start))).toString()+"px "+(M*h+.5*n).toString()+"px"}).attr("class","exclude-range")}l(Z,"drawExcludeDays");function K(h,g,p,k){if(p<=0||h>g)return 1/0;const n=g-h,d=W.duration({[k??"day"]:p}).asMilliseconds();return d<=0?1/0:Math.ceil(n/d)}l(K,"getEstimatedTickCount");function E(h,g,p,k){const n=e.db.getDateFormat(),d=e.db.getAxisFormat();let f;d?f=d:n==="D"?f="%d":f=a.axisFormat??"%Y-%m-%d";let u=_e(C).tickSize(-k+g+a.gridLineStartPadding).tickFormat(Nt(f));const s=/^([1-9]\d*)(millisecond|second|minute|hour|day|week|month)$/.exec(e.db.getTickInterval()||a.tickInterval);if(s!==null){const D=parseInt(s[1],10);if(isNaN(D)||D<=0)st.warn(`Invalid tick interval value: "${s[1]}". Skipping custom tick interval.`);else{const c=s[2],R=e.db.getWeekday()||a.weekday,o=C.domain(),x=o[0],b=o[1],M=K(x,b,D,c);if(M>_t)st.warn(`The tick interval "${D}${c}" would generate ${M} ticks, which exceeds the maximum allowed (${_t}). This may indicate an invalid date or time range. Skipping custom tick interval.`);else switch(c){case"millisecond":u.ticks(Xt.every(D));break;case"second":u.ticks(Ht.every(D));break;case"minute":u.ticks(qt.every(D));break;case"hour":u.ticks(jt.every(D));break;case"day":u.ticks(zt.every(D));break;case"week":u.ticks(Jt[R].every(D));break;case"month":u.ticks(Bt.every(D));break}}}if(V.append("g").attr("class","grid").attr("transform","translate("+h+", "+(k-50)+")").call(u).selectAll("text").style("text-anchor","middle").attr("fill","#000").attr("stroke","none").attr("font-size",10).attr("dy","1em"),e.db.topAxisEnabled()||a.topAxis){let D=Fe(C).tickSize(-k+g+a.gridLineStartPadding).tickFormat(Nt(f));if(s!==null){const c=parseInt(s[1],10);if(isNaN(c)||c<=0)st.warn(`Invalid tick interval value: "${s[1]}". Skipping custom tick interval.`);else{const R=s[2],o=e.db.getWeekday()||a.weekday,x=C.domain(),b=x[0],M=x[1];if(K(b,M,c,R)<=_t)switch(R){case"millisecond":D.ticks(Xt.every(c));break;case"second":D.ticks(Ht.every(c));break;case"minute":D.ticks(qt.every(c));break;case"hour":D.ticks(jt.every(c));break;case"day":D.ticks(zt.every(c));break;case"week":D.ticks(Jt[o].every(c));break;case"month":D.ticks(Bt.every(c));break}}}V.append("g").attr("class","grid").attr("transform","translate("+h+", "+g+")").call(D).selectAll("text").style("text-anchor","middle").attr("fill","#000").attr("stroke","none").attr("font-size",10)}}l(E,"makeGrid");function v(h,g){let p=0;const k=Object.keys(P).map(n=>[n,P[n]]);V.append("g").selectAll("text").data(k).enter().append(function(n){const d=n[0].split(ke.lineBreakRegex),f=-(d.length-1)/2,u=O.createElementNS("http://www.w3.org/2000/svg","text");u.setAttribute("dy",f+"em");for(const[_,s]of d.entries()){const D=O.createElementNS("http://www.w3.org/2000/svg","tspan");D.setAttribute("alignment-baseline","central"),D.setAttribute("x","10"),_>0&&D.setAttribute("dy","1em"),D.textContent=s,u.appendChild(D)}return u}).attr("x",10).attr("y",function(n,d){if(d>0)for(let f=0;f<d;f++)return p+=k[d-1][1],n[1]*h/2+p*h+g;else return n[1]*h/2+g}).attr("font-size",a.sectionFontSize).attr("class",function(n){for(const[d,f]of $.entries())if(n[0]===f)return"sectionTitle sectionTitle"+d%a.numberSectionStyles;return"sectionTitle"})}l(v,"vertLabels");function m(h,g,p,k){const n=e.db.getTodayMarker();if(n==="off")return;const d=V.append("g").attr("class","today"),f=new Date,u=d.append("line");u.attr("x1",C(f)+h).attr("x2",C(f)+h).attr("y1",a.titleTopMargin).attr("y2",k-a.titleTopMargin).attr("class","today"),n!==""&&u.attr("style",n.replace(/,/g,";"))}l(m,"drawToday");function I(h){const g={},p=[];for(let k=0,n=h.length;k<n;++k)Object.prototype.hasOwnProperty.call(g,h[k])||(g[h[k]]=!0,p.push(h[k]));return p}l(I,"checkUnique")},"draw"),Es={setConf:Ds,draw:Ss},Is=l(t=>`
  .mermaid-main-font {
        font-family: ${t.fontFamily};
  }

  .exclude-range {
    fill: ${t.excludeBkgColor};
  }

  .section {
    stroke: none;
    opacity: 0.2;
  }

  .section0 {
    fill: ${t.sectionBkgColor};
  }

  .section2 {
    fill: ${t.sectionBkgColor2};
  }

  .section1,
  .section3 {
    fill: ${t.altSectionBkgColor};
    opacity: 0.2;
  }

  .sectionTitle0 {
    fill: ${t.titleColor};
  }

  .sectionTitle1 {
    fill: ${t.titleColor};
  }

  .sectionTitle2 {
    fill: ${t.titleColor};
  }

  .sectionTitle3 {
    fill: ${t.titleColor};
  }

  .sectionTitle {
    text-anchor: start;
    font-family: ${t.fontFamily};
  }


  /* Grid and axis */

  .grid .tick {
    stroke: ${t.gridColor};
    opacity: 0.8;
    shape-rendering: crispEdges;
  }

  .grid .tick text {
    font-family: ${t.fontFamily};
    fill: ${t.textColor};
  }

  .grid path {
    stroke-width: 0;
  }


  /* Today line */

  .today {
    fill: none;
    stroke: ${t.todayLineColor};
    stroke-width: 2px;
  }


  /* Task styling */

  /* Default task */

  .task {
    stroke-width: 2;
  }

  .taskText {
    text-anchor: middle;
    font-family: ${t.fontFamily};
  }

  .taskTextOutsideRight {
    fill: ${t.taskTextDarkColor};
    text-anchor: start;
    font-family: ${t.fontFamily};
  }

  .taskTextOutsideLeft {
    fill: ${t.taskTextDarkColor};
    text-anchor: end;
  }


  /* Special case clickable */

  .task.clickable {
    cursor: pointer;
  }

  .taskText.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideLeft.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideRight.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }


  /* Specific task settings for the sections*/

  .taskText0,
  .taskText1,
  .taskText2,
  .taskText3 {
    fill: ${t.taskTextColor};
  }

  .task0,
  .task1,
  .task2,
  .task3 {
    fill: ${t.taskBkgColor};
    stroke: ${t.taskBorderColor};
  }

  .taskTextOutside0,
  .taskTextOutside2
  {
    fill: ${t.taskTextOutsideColor};
  }

  .taskTextOutside1,
  .taskTextOutside3 {
    fill: ${t.taskTextOutsideColor};
  }


  /* Active task */

  .active0,
  .active1,
  .active2,
  .active3 {
    fill: ${t.activeTaskBkgColor};
    stroke: ${t.activeTaskBorderColor};
  }

  .activeText0,
  .activeText1,
  .activeText2,
  .activeText3 {
    fill: ${t.taskTextDarkColor} !important;
  }


  /* Completed task */

  .done0,
  .done1,
  .done2,
  .done3 {
    stroke: ${t.doneTaskBorderColor};
    fill: ${t.doneTaskBkgColor};
    stroke-width: 2;
  }

  .doneText0,
  .doneText1,
  .doneText2,
  .doneText3 {
    fill: ${t.taskTextDarkColor} !important;
  }

  /* Done task text displayed outside the bar sits against the diagram background,
     not against the done-task bar, so it must use the outside/contrast color. */
  .doneText0.taskTextOutsideLeft,
  .doneText0.taskTextOutsideRight,
  .doneText1.taskTextOutsideLeft,
  .doneText1.taskTextOutsideRight,
  .doneText2.taskTextOutsideLeft,
  .doneText2.taskTextOutsideRight,
  .doneText3.taskTextOutsideLeft,
  .doneText3.taskTextOutsideRight {
    fill: ${t.taskTextOutsideColor} !important;
  }


  /* Tasks on the critical line */

  .crit0,
  .crit1,
  .crit2,
  .crit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.critBkgColor};
    stroke-width: 2;
  }

  .activeCrit0,
  .activeCrit1,
  .activeCrit2,
  .activeCrit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.activeTaskBkgColor};
    stroke-width: 2;
  }

  .doneCrit0,
  .doneCrit1,
  .doneCrit2,
  .doneCrit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.doneTaskBkgColor};
    stroke-width: 2;
    cursor: pointer;
    shape-rendering: crispEdges;
  }

  .milestone {
    transform: rotate(45deg) scale(0.8,0.8);
  }

  .milestoneText {
    font-style: italic;
  }
  .doneCritText0,
  .doneCritText1,
  .doneCritText2,
  .doneCritText3 {
    fill: ${t.taskTextDarkColor} !important;
  }

  /* Done-crit task text outside the bar — same reasoning as doneText above. */
  .doneCritText0.taskTextOutsideLeft,
  .doneCritText0.taskTextOutsideRight,
  .doneCritText1.taskTextOutsideLeft,
  .doneCritText1.taskTextOutsideRight,
  .doneCritText2.taskTextOutsideLeft,
  .doneCritText2.taskTextOutsideRight,
  .doneCritText3.taskTextOutsideLeft,
  .doneCritText3.taskTextOutsideRight {
    fill: ${t.taskTextOutsideColor} !important;
  }

  .vert {
    stroke: ${t.vertLineColor};
  }

  .vertText {
    font-size: 15px;
    text-anchor: middle;
    fill: ${t.vertLineColor} !important;
  }

  .activeCritText0,
  .activeCritText1,
  .activeCritText2,
  .activeCritText3 {
    fill: ${t.taskTextDarkColor} !important;
  }

  .titleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${t.titleColor||t.textColor};
    font-family: ${t.fontFamily};
  }
`,"getStyles"),Ms=Is,Ns={parser:Ne,db:_s,renderer:Es,styles:Ms};export{Ns as diagram};
