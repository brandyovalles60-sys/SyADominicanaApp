;!function(){try { var e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof global?global:"undefined"!=typeof window?window:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&((e._debugIds|| (e._debugIds={}))[n]="7e44b0f9-0538-9684-f9ef-cad7b271713a")}catch(e){}}();
(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,749199,e=>{"use strict";var t=e.i(242882),s=e.i(820308),a=e.i(150671),r=e.i(714403),n=e.i(635494),o=e.i(189329);e.s(["default",0,({sql:e,params:i=s.DEFAULT_QUERY_PARAMS,where:l,orderBy:c})=>{let{data:u}=(0,n.useSelectedProjectQuery)(),d=(0,o.useDatabaseSelectorStateSnapshot)(),{data:m}=(0,a.useReadReplicasQuery)({projectRef:u?.ref}),p=(m||[]).find(e=>e.identifier===d.selectedDatabaseId)?.connectionString,_=d.selectedDatabaseId,h="function"==typeof e?e([]):e,{data:g,error:f,isPending:x,isRefetching:y,refetch:b}=(0,t.useQuery)({queryKey:["projects",u?.ref,"db",{...i,sql:h,identifier:_},l,c],queryFn:({signal:e})=>(0,r.executeSql)({projectRef:u?.ref,connectionString:p||u?.connectionString,sql:h},e).then(e=>e.result),enabled:!!h,refetchOnWindowFocus:!1,refetchOnReconnect:!1});return{error:f||("object"==typeof g?g?.error:""),data:g,isLoading:x,isRefetching:y,params:i,runQuery:b,resolvedSql:h}}])},888525,760255,284399,e=>{"use strict";var t=e.i(355901),s=e.i(714403),a=e.i(392491);function r(e=[]){return{hypopg:e.find(e=>"hypopg"===e.name),indexAdvisor:e.find(e=>"index_advisor"===e.name)}}function n(e,t){return void 0===e||void 0===t||e<=0||e<=t?0:(e-t)/e*100}async function o({projectRef:e,connectionString:a,indexStatements:r,onSuccess:n,onError:o}){if(!e){let e=Error("Project ref is required");return o&&o(e),Promise.reject(e)}if(0===r.length){let e=Error("No index statements provided");return o&&o(e),Promise.reject(e)}try{return await (0,s.executeSql)({projectRef:e,connectionString:a,sql:r.join(";\n")+";"}),t.toast.success("Successfully created index"),n&&n(),Promise.resolve()}catch(e){return t.toast.error(`Failed to create index: ${e.message}`),o&&o(e),Promise.reject(e)}}function i(e,t){return!!(t&&e?.index_statements&&e.index_statements.length>0)}function l(e){return e&&0!==e.length?e.filter(e=>{let t=e.match(/ON\s+(?:"?(\w+)"?\.|(\w+)\.)/i);if(!t)return!0;let s=t[1]||t[2];return!s||!a.INTERNAL_SCHEMAS.includes(s.toLowerCase())}):[]}function c(e){if(!e||!e.index_statements)return e??null;let t=l(e.index_statements);return 0===t.length?null:{...e,index_statements:t}}function u(e){if(!e)return!1;let t=e.toLowerCase();return a.INTERNAL_SCHEMAS.some(e=>RegExp(`(?:from|join|update|insert\\s+into|delete\\s+from)\\s+(?:${e}\\.|"${e}"\\.)`,"i").test(t))}e.s(["calculateImprovement",()=>n,"createIndexes",()=>o,"filterProtectedSchemaIndexAdvisorResult",()=>c,"filterProtectedSchemaIndexStatements",()=>l,"getIndexAdvisorExtensions",()=>r,"hasIndexRecommendations",()=>i,"queryInvolvesProtectedSchemas",()=>u],760255);var d=e.i(450972),m=e.i(635494);function p(){let{data:e}=(0,m.useSelectedProjectQuery)(),{data:t}=(0,d.useDatabaseExtensionsQuery)({projectRef:e?.ref,connectionString:e?.connectionString}),{hypopg:s,indexAdvisor:a}=r(t??[]),n=!!s&&!!a,o=n&&null!==s.installed_version&&null!==a.installed_version;return{isIndexAdvisorAvailable:n,isIndexAdvisorEnabled:o}}e.s(["useIndexAdvisorStatus",()=>p],888525);var _=e.i(478902),h=e.i(389959),g=e.i(610144),f=e.i(967052),x=e.i(232520),y=e.i(837710);e.s(["EnableIndexAdvisorButton",0,()=>{let e=(0,f.useTrack)(),{data:s}=(0,m.useSelectedProjectQuery)(),[a,n]=(0,h.useState)(!1),{data:o}=(0,d.useDatabaseExtensionsQuery)({projectRef:s?.ref,connectionString:s?.connectionString}),{hypopg:i,indexAdvisor:l}=r(o),{mutateAsync:c,isPending:u}=(0,g.useDatabaseExtensionEnableMutation)(),p=async()=>{if(void 0===s)return t.toast.error("Project is required");try{i?.installed_version===null&&await c({projectRef:s?.ref,connectionString:s?.connectionString,name:i.name,schema:i?.schema??"extensions",version:i.default_version}),l?.installed_version===null&&await c({projectRef:s?.ref,connectionString:s?.connectionString,name:l.name,schema:l?.schema??"extensions",version:l.default_version}),t.toast.success("Successfully enabled Index Advisor!"),n(!1)}catch(e){t.toast.error(`Failed to enable Index Advisor: ${e.message}`)}};return(0,_.jsxs)(x.AlertDialog,{open:a,onOpenChange:()=>n(!a),children:[(0,_.jsx)(x.AlertDialogTrigger,{asChild:!0,children:(0,_.jsx)(y.Button,{type:"primary",onClick:()=>e("index_advisor_banner_enable_button_clicked"),children:"Enable"})}),(0,_.jsxs)(x.AlertDialogContent,{children:[(0,_.jsxs)(x.AlertDialogHeader,{children:[(0,_.jsx)(x.AlertDialogTitle,{children:"Enable Index Advisor"}),(0,_.jsxs)(x.AlertDialogDescription,{children:["This will enable the ",(0,_.jsx)("code",{className:"text-code-inline",children:"index_advisor"})," and"," ",(0,_.jsx)("code",{className:"text-code-inline",children:"hypopg"})," Postgres extensions so Index Advisor can analyse queries and suggest performance-improving indexes."]})]}),(0,_.jsxs)(x.AlertDialogFooter,{children:[(0,_.jsx)(x.AlertDialogCancel,{children:"Cancel"}),(0,_.jsx)(x.AlertDialogAction,{onClick:t=>{t.preventDefault(),p(),e("index_advisor_dialog_enable_button_clicked")},disabled:u,children:u?"Enabling...":"Enable"})]})]})]})}],284399)},610144,e=>{"use strict";var t=e.i(850036),s=e.i(479084),a=e.i(38429),r=e.i(356003),n=e.i(355901),o=e.i(78162),i=e.i(714403),l=e.i(667286);async function c({projectRef:e,connectionString:a,schema:r,name:n,version:o,cascade:l=!1,createSchema:c=!1}){let u=new Headers;a&&u.set("x-connection-encrypted",a);let{sql:d}=t.default.extensions.create({schema:r,name:n,version:o,cascade:l}),{result:m}=await (0,i.executeSql)({projectRef:e,connectionString:a,sql:c?`create schema if not exists ${(0,s.ident)(r)}; ${d}`:d,queryKey:["extension","create"]});return m}e.s(["useDatabaseExtensionEnableMutation",0,({onSuccess:e,onError:t,...s}={})=>{let i=(0,r.useQueryClient)();return(0,a.useMutation)({mutationFn:e=>c(e),async onSuccess(t,s,a){let{projectRef:r}=s;await Promise.all([i.invalidateQueries({queryKey:l.databaseExtensionsKeys.list(r)}),i.invalidateQueries({queryKey:o.configKeys.upgradeEligibility(r)})]),await e?.(t,s,a)},async onError(e,s,a){void 0===t?n.toast.error(`Failed to enable database extension: ${e.message}`):t(e,s,a)},...s})}])},820308,775159,e=>{"use strict";var t,s,a=e.i(55956),r=((t={}).API="api",t.STORAGE="storage",t.AUTH="auth",t.QUERY_PERFORMANCE="query_performance",t.DATABASE="database",t);e.s(["Presets",()=>r],775159);var n=((s={}).LAST_10_MINUTES="Last 10 minutes",s.LAST_30_MINUTES="Last 30 minutes",s.LAST_60_MINUTES="Last 60 minutes",s.LAST_3_HOURS="Last 3 hours",s.LAST_24_HOURS="Last 24 hours",s.LAST_7_DAYS="Last 7 days",s.LAST_14_DAYS="Last 14 days",s.LAST_28_DAYS="Last 28 days",s);let o=[{text:"Last 10 minutes",calcFrom:()=>(0,a.default)().subtract(10,"minute").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["free","pro","team","enterprise","platform"]},{text:"Last 30 minutes",calcFrom:()=>(0,a.default)().subtract(30,"minute").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["free","pro","team","enterprise","platform"]},{text:"Last 60 minutes",calcFrom:()=>(0,a.default)().subtract(1,"hour").toISOString(),calcTo:()=>(0,a.default)().toISOString(),default:!0,availableIn:["free","pro","team","enterprise","platform"]},{text:"Last 3 hours",calcFrom:()=>(0,a.default)().subtract(3,"hour").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["free","pro","team","enterprise","platform"]},{text:"Last 24 hours",calcFrom:()=>(0,a.default)().subtract(1,"day").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["free","pro","team","enterprise","platform"]},{text:"Last 7 days",calcFrom:()=>(0,a.default)().subtract(7,"day").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["pro","team","enterprise"]},{text:"Last 14 days",calcFrom:()=>(0,a.default)().subtract(14,"day").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["team","enterprise"]},{text:"Last 28 days",calcFrom:()=>(0,a.default)().subtract(28,"day").toISOString(),calcTo:()=>(0,a.default)().toISOString(),availableIn:["team","enterprise"]}],i={iso_timestamp_start:o[0].calcFrom(),iso_timestamp_end:o[0].calcTo()},l=(e,t=!0)=>{if(0===e.length)return"";let s=e.map(e=>{let t=e.key.split("."),s=[t[t.length-2],t[t.length-1]].join("."),a=e.key.includes(".")?s:e.key,r=e.value.toString().includes('"')||e.value.toString().includes("'"),n=!isNaN(Number(e.value)),o=!n&&r?e.value:`'${e.value}'`,i=!n&&String(o).toLowerCase(),l=n?e.value:i;switch(e.compare){case"matches":return`REGEXP_CONTAINS(${a}, ${l})`;case"is":default:return`${a} = ${l}`;case"!=":return`${a} != ${l}`;case">=":return`${a} >= ${l}`;case"<=":return`${a} <= ${l}`;case">":return`${a} > ${l}`;case"<":return`${a} < ${l}`}}).filter(Boolean).join(" AND ");return""===s?"":t?"WHERE "+s:"AND "+s},c={[r.API]:{title:"API",queries:{totalRequests:{queryType:"logs",sql:e=>`
        -- reports-api-total-requests
        select
          cast(timestamp_trunc(t.timestamp, hour) as datetime) as timestamp,
          count(t.id) as count
        FROM edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
          ${l(e)}
        GROUP BY
          timestamp
        ORDER BY
          timestamp ASC`},topRoutes:{queryType:"logs",sql:e=>`
        -- reports-api-top-routes
        select
          request.path as path,
          request.method as method,
          request.search as search,
          response.status_code as status_code,
          count(t.id) as count
        from edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
          ${l(e)}
        group by
          request.path, request.method, request.search, response.status_code
        order by
          count desc
        limit 10
        `},errorCounts:{queryType:"logs",sql:e=>`
        -- reports-api-error-counts
        select
          cast(timestamp_trunc(t.timestamp, hour) as datetime) as timestamp,
          count(t.id) as count
        FROM edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
        WHERE
          response.status_code >= 400
        ${l(e,!1)}
        GROUP BY
          timestamp
        ORDER BY
          timestamp ASC
        `},topErrorRoutes:{queryType:"logs",sql:e=>`
        -- reports-api-top-error-routes
        select
          request.path as path,
          request.method as method,
          request.search as search,
          response.status_code as status_code,
          count(t.id) as count
        from edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
        where
          response.status_code >= 400
        ${l(e,!1)}
        group by
          request.path, request.method, request.search, response.status_code
        order by
          count desc
        limit 10
        `},responseSpeed:{queryType:"logs",sql:e=>`
        -- reports-api-response-speed
        select
          cast(timestamp_trunc(t.timestamp, hour) as datetime) as timestamp,
          avg(response.origin_time) as avg
        FROM
          edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
          ${l(e)}
        GROUP BY
          timestamp
        ORDER BY
          timestamp ASC
      `},topSlowRoutes:{queryType:"logs",sql:e=>`
        -- reports-api-top-slow-routes
        select
          request.path as path,
          request.method as method,
          request.search as search,
          response.status_code as status_code,
          count(t.id) as count,
          avg(response.origin_time) as avg
        from edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
        ${l(e)}
        group by
          request.path, request.method, request.search, response.status_code
        order by
          avg desc
        limit 10
        `},networkTraffic:{queryType:"logs",sql:e=>`
        -- reports-api-network-traffic
        select
          cast(timestamp_trunc(t.timestamp, hour) as datetime) as timestamp,
          coalesce(
            safe_divide(
              sum(
                cast(coalesce(headers.content_length, "0") as int64)
              ),
              1000000
            ),
            0
          ) as ingress_mb,
          coalesce(
            safe_divide(
              sum(
                cast(coalesce(resp_headers.content_length, "0") as int64)
              ),
              1000000
            ),
            0
          ) as egress_mb,
        FROM
          edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
          cross join unnest(response.headers) as resp_headers
          ${l(e)}
        GROUP BY
          timestamp
        ORDER BY
          timestamp ASC
        `},requestsByCountry:{queryType:"logs",sql:e=>`
        -- reports-api-requests-by-country
        select
          cf.country as country,
          count(t.id) as count
        from edge_logs t
          cross join unnest(metadata) as m
          cross join unnest(m.response) as response
          cross join unnest(m.request) as request
          cross join unnest(request.headers) as headers
          cross join unnest(request.cf) as cf
        where
          cf.country is not null
        ${l(e,!1)}
        group by
          cf.country
        `}}},[r.AUTH]:{title:"",queries:{}},[r.STORAGE]:{title:"Storage",queries:{cacheHitRate:{queryType:"logs",sql:e=>`
        -- reports-storage-cache-hit-rate
SELECT
  timestamp_trunc(timestamp, hour) as timestamp,
  countif( h.cf_cache_status in ('HIT', 'STALE', 'REVALIDATED', 'UPDATING') ) as hit_count,
  countif( h.cf_cache_status in ('MISS', 'NONE/UNKNOWN', 'EXPIRED', 'BYPASS', 'DYNAMIC') ) as miss_count
from edge_logs f
  cross join unnest(f.metadata) as m
  cross join unnest(m.request) as r
  cross join unnest(m.response) as res
  cross join unnest(res.headers) as h
where starts_with(r.path, '/storage/v1/object') and r.method = 'GET'
  ${l(e,!1)}
group by timestamp
order by timestamp desc
`},topCacheMisses:{queryType:"logs",sql:e=>`
        -- reports-storage-top-cache-misses
SELECT
  r.path as path,
  r.search as search,
  count(id) as count
from edge_logs f
  cross join unnest(f.metadata) as m
  cross join unnest(m.request) as r
  cross join unnest(m.response) as res
  cross join unnest(res.headers) as h
where starts_with(r.path, '/storage/v1/object')
  and r.method = 'GET'
  and h.cf_cache_status in ('MISS', 'NONE/UNKNOWN', 'EXPIRED', 'BYPASS', 'DYNAMIC')
  ${l(e,!1)}
group by path, search
order by count desc
limit 12
    `}}},[r.QUERY_PERFORMANCE]:{title:"Query performance",queries:{mostFrequentlyInvoked:{queryType:"db",sql:(e,t,s,a=!1,r=!1)=>`
        -- reports-query-performance-most-frequently-invoked
set search_path to public, extensions;

select
    auth.rolname,
    statements.query,
    statements.calls,
    -- -- Postgres 13, 14, 15
    statements.total_exec_time + statements.total_plan_time as total_time,
    statements.min_exec_time + statements.min_plan_time as min_time,
    statements.max_exec_time + statements.max_plan_time as max_time,
    statements.mean_exec_time + statements.mean_plan_time as mean_time,
    -- -- Postgres <= 12
    -- total_time,
    -- min_time,
    -- max_time,
    -- mean_time,
    coalesce(statements.rows::numeric / nullif(statements.calls, 0), 0) as avg_rows,
    statements.rows as rows_read,
    case
      when (statements.shared_blks_hit + statements.shared_blks_read) > 0
      then round(
        (statements.shared_blks_hit * 100.0) /
        (statements.shared_blks_hit + statements.shared_blks_read),
        2
      )
      else 0
    end as cache_hit_rate${a?`,
    case
      when (lower(statements.query) like 'select%' or lower(statements.query) like 'with pgrst%')
      then (
        select json_build_object(
          'has_suggestion', array_length(index_statements, 1) > 0,
          'startup_cost_before', startup_cost_before,
          'startup_cost_after', startup_cost_after,
          'total_cost_before', total_cost_before,
          'total_cost_after', total_cost_after,
          'index_statements', index_statements
        )
        from index_advisor(statements.query)
      )
      else null
    end as index_advisor_result`:""}
  from pg_stat_statements as statements
    inner join pg_authid as auth on statements.userid = auth.oid
  -- skip queries that were never actually executed
  WHERE statements.calls > 0 ${t?t.replace(/^WHERE/,"AND"):""}
  ${s||"order by statements.calls desc"}
  limit 20`},mostTimeConsuming:{queryType:"db",sql:(e,t,s,a=!1,r=!1)=>`
        -- reports-query-performance-most-time-consuming
set search_path to public, extensions;

-- compute total time once up front so we don't need a window function over all rows
with grand_total as (
  select coalesce(nullif(sum(total_exec_time + total_plan_time), 0), 1) as v
  from pg_stat_statements where calls > 0
)
select
    auth.rolname,
    statements.query,
    statements.calls,
    statements.total_exec_time + statements.total_plan_time as total_time,
    statements.mean_exec_time + statements.mean_plan_time as mean_time,
    coalesce(
      ((statements.total_exec_time + statements.total_plan_time) /
        (select v from grand_total)) *
        100,
      0
    ) as prop_total_time${a?`,
    case
      when (lower(statements.query) like 'select%' or lower(statements.query) like 'with pgrst%')
      then (
        select json_build_object(
          'has_suggestion', array_length(index_statements, 1) > 0,
          'startup_cost_before', startup_cost_before,
          'startup_cost_after', startup_cost_after,
          'total_cost_before', total_cost_before,
          'total_cost_after', total_cost_after,
          'index_statements', index_statements
        )
        from index_advisor(statements.query)
      )
      else null
    end as index_advisor_result`:""}
  from pg_stat_statements as statements
    inner join pg_authid as auth on statements.userid = auth.oid
  -- skip queries that were never actually executed
  WHERE statements.calls > 0 ${t?t.replace(/^WHERE/,"AND"):""}
  ${s||"order by total_time desc"}
  limit 20`},slowestExecutionTime:{queryType:"db",sql:(e,t,s,a=!1,r=!1)=>`
        -- reports-query-performance-slowest-execution-time
set search_path to public, extensions;

select
    auth.rolname,
    statements.query,
    statements.calls,
    -- -- Postgres 13, 14, 15
    statements.total_exec_time + statements.total_plan_time as total_time,
    statements.min_exec_time + statements.min_plan_time as min_time,
    statements.max_exec_time + statements.max_plan_time as max_time,
    statements.mean_exec_time + statements.mean_plan_time as mean_time,
    -- -- Postgres <= 12
    -- total_time,
    -- min_time,
    -- max_time,
    -- mean_time,
    coalesce(statements.rows::numeric / nullif(statements.calls, 0), 0) as avg_rows${a?`,
    case
      when (lower(statements.query) like 'select%' or lower(statements.query) like 'with pgrst%')
      then (
        select json_build_object(
          'has_suggestion', array_length(index_statements, 1) > 0,
          'startup_cost_before', startup_cost_before,
          'startup_cost_after', startup_cost_after,
          'total_cost_before', total_cost_before,
          'total_cost_after', total_cost_after,
          'index_statements', index_statements
        )
        from index_advisor(statements.query)
      )
      else null
    end as index_advisor_result`:""}
  from pg_stat_statements as statements
    inner join pg_authid as auth on statements.userid = auth.oid
  -- skip queries that were never actually executed
  WHERE statements.calls > 0 ${t?t.replace(/^WHERE/,"AND"):""}
  ${s||"order by max_time desc"}
  limit 20`},queryHitRate:{queryType:"db",sql:e=>`-- reports-query-performance-cache-and-index-hit-rate
select
    'index hit rate' as name,
    (sum(idx_blks_hit)) / nullif(sum(idx_blks_hit + idx_blks_read),0) as ratio
  from pg_statio_user_indexes
  union all
  select
    'table hit rate' as name,
    sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read),0) as ratio
  from pg_statio_user_tables;`},unified:{queryType:"db",sql:(e,t,s,a=!1,r=!1)=>`
        -- reports-query-performance-unified
        set search_path to public, extensions;

        -- compute total time once up front so we don't need a window function over all rows
        with grand_total as (
          select coalesce(nullif(sum(total_exec_time + total_plan_time), 0), 1) as v
          from pg_stat_statements where calls > 0
        ),
        base as (
          select
            auth.rolname,
            statements.query,
            statements.calls,
            statements.total_exec_time + statements.total_plan_time as total_time,
            statements.min_exec_time + statements.min_plan_time as min_time,
            statements.max_exec_time + statements.max_plan_time as max_time,
            statements.mean_exec_time + statements.mean_plan_time as mean_time,
            coalesce(statements.rows::numeric / nullif(statements.calls, 0), 0) as avg_rows,
            statements.rows as rows_read,
            statements.shared_blks_hit as debug_hit,
            statements.shared_blks_read as debug_read,
            case
              when (statements.shared_blks_hit + statements.shared_blks_read) > 0
              then (statements.shared_blks_hit::numeric * 100.0) /
                   (statements.shared_blks_hit + statements.shared_blks_read)
              else 0
            end as cache_hit_rate,
            coalesce(
              ((statements.total_exec_time + statements.total_plan_time) /
                (select v from grand_total)) *
                100,
              0
            ) as prop_total_time
          from pg_stat_statements as statements
            inner join pg_authid as auth on statements.userid = auth.oid
          -- skip queries that were never actually executed
          WHERE statements.calls > 0 ${t?t.replace(/^WHERE/,"AND"):""}
          ${s||"order by total_time desc"}
          limit 50
        ),
        query_results as (
          select
            base.*${a?`,
            case
              when (lower(base.query) like 'select%' or lower(base.query) like 'with pgrst%')
              then (
                select json_build_object(
                  'has_suggestion', array_length(index_statements, 1) > 0,
                  'startup_cost_before', startup_cost_before,
                  'startup_cost_after', startup_cost_after,
                  'total_cost_before', total_cost_before,
                  'total_cost_after', total_cost_after,
                  'index_statements', index_statements
                )
                from index_advisor(base.query)
              )
              else null
            end as index_advisor_result`:""}
          from base
        )
        select *
        from query_results
        ${r&&a?"where (index_advisor_result->>'has_suggestion')::boolean = true":""}
        ${s||"order by total_time desc"}
        limit 20`},slowQueriesCount:{queryType:"db",sql:()=>`
        -- reports-query-performance-slow-queries-count
        set search_path to public, extensions;

        -- Count of slow queries (> 1 second average)
        SELECT count(*) as slow_queries_count
        -- alias needed to reference columns in WHERE
        FROM pg_stat_statements as statements
        -- skip never-executed queries; mean_exec_time > 1000ms = avg over 1 second
        WHERE statements.calls > 0 AND statements.mean_exec_time > 1000;`},queryMetrics:{queryType:"db",sql:(e,t,s,a=!1,r=!1)=>`
        -- reports-query-performance-metrics
        set search_path to public, extensions;

        SELECT
          COALESCE(ROUND(AVG(statements.rows::numeric / NULLIF(statements.calls, 0)), 1), 0) as avg_rows_per_call,
          COUNT(*) FILTER (WHERE statements.total_exec_time + statements.total_plan_time > 1000) as slow_queries,
          COALESCE(
            ROUND(
              SUM(statements.shared_blks_hit) * 100.0 /
              NULLIF(SUM(statements.shared_blks_hit + statements.shared_blks_read), 0),
              2
            ), 0
          ) || '%' as cache_hit_rate
        FROM pg_stat_statements as statements
        -- skip queries that were never actually executed
        WHERE statements.calls > 0 ${t?t.replace(/^WHERE/,"AND"):""}
        ${s||""}`}}},[r.DATABASE]:{title:"database",queries:{largeObjects:{queryType:"db",sql:e=>`-- reports-database-large-objects
SELECT
        SCHEMA_NAME,
        relname,
        table_size
      FROM
        (SELECT
          pg_catalog.pg_namespace.nspname AS SCHEMA_NAME,
          relname,
          pg_total_relation_size(pg_catalog.pg_class.oid) AS table_size
        FROM pg_catalog.pg_class
        JOIN pg_catalog.pg_namespace ON relnamespace = pg_catalog.pg_namespace.oid
        ) t
      WHERE SCHEMA_NAME NOT LIKE 'pg_%'
      ORDER BY table_size DESC
      LIMIT 5;`}}}};e.s(["DEFAULT_QUERY_PARAMS",0,i,"DEPRECATED_REPORTS",0,["total_realtime_ingress","total_rest_options_requests","total_auth_ingress","total_auth_get_requests","total_auth_post_requests","total_auth_patch_requests","total_auth_options_requests","total_storage_options_requests","total_storage_patch_requests","total_options_requests","total_rest_ingress","total_rest_get_requests","total_rest_post_requests","total_rest_patch_requests","total_rest_delete_requests","total_storage_get_requests","total_storage_post_requests","total_storage_delete_requests","total_auth_delete_requests","total_get_requests","total_patch_requests","total_post_requests","total_ingress","total_delete_requests"],"EDGE_FUNCTION_REGIONS",0,[{key:"ap-northeast-1",label:"Tokyo"},{key:"ap-northeast-2",label:"Seoul"},{key:"ap-south-1",label:"Mumbai"},{key:"ap-southeast-1",label:"Singapore"},{key:"ap-southeast-2",label:"Sydney"},{key:"ca-central-1",label:"Canada Central"},{key:"us-east-1",label:"N. Virginia"},{key:"us-west-1",label:"N. California"},{key:"us-west-2",label:"Oregon"},{key:"eu-central-1",label:"Frankfurt"},{key:"eu-west-1",label:"Ireland"},{key:"eu-west-2",label:"London"},{key:"eu-west-3",label:"Paris"},{key:"sa-east-1",label:"São Paulo"}],"LAYOUT_COLUMN_COUNT",0,2,"PRESET_CONFIG",0,c,"REPORTS_DATEPICKER_HELPERS",0,o,"REPORT_DATERANGE_HELPER_LABELS",()=>n,"generateRegexpWhere",0,l],820308)},670447,e=>{"use strict";var t=e.i(478902),s=e.i(975924),a=e.i(837710),r=e.i(627069),n=e.i(843778),o=e.i(10429);e.s(["BannerCard",0,({onDismiss:e,children:i,className:l})=>(0,t.jsxs)(r.Card,{className:(0,n.cn)("relative overflow-hidden shadow-lg rounded-2xl",l),children:[(0,t.jsxs)("div",{className:"absolute -inset-16 z-0 opacity-100 pointer-events-none",children:[(0,t.jsx)("img",{src:`${o.BASE_PATH}/img/reports/bg-grafana-dark.svg`,alt:"Background pattern",className:"w-full h-full object-cover object-right hidden dark:block"}),(0,t.jsx)("img",{src:`${o.BASE_PATH}/img/reports/bg-grafana-light.svg`,alt:"Background pattern",className:"w-full h-full object-cover object-right dark:hidden"}),(0,t.jsx)("div",{className:"absolute inset-0 bg-gradient-to-r from-background-alternative to-transparent"})]}),(0,t.jsxs)(r.CardContent,{className:"relative z-10 p-6",children:[e&&(0,t.jsx)("div",{className:"absolute top-4 right-4 z-20",children:(0,t.jsx)(a.Button,{type:"text",size:"tiny",htmlType:"button",icon:(0,t.jsx)(s.X,{size:16,strokeWidth:1.5}),onClick:t=>{t.preventDefault(),e()},className:"opacity-75 hover:opacity-100 px-1","aria-label":"Close banner"})}),i]})]})])},582391,e=>{"use strict";let t=(0,e.i(388019).default)("Pen",[["path",{d:"M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z",key:"1a8usu"}]]);e.s(["Edit2",()=>t],582391)},256337,303213,e=>{"use strict";var t=e.i(478902),s=e.i(934302);e.i(128328);var a=e.i(657588),r=e.i(158639),n=e.i(629541),o=e.i(389959),i=e.i(355901),l=e.i(420985),c=e.i(635494),u=e.i(48189),d=e.i(432478),m=e.i(837710),p=e.i(441345),_=e.i(171997),h=e.i(40892);let g=({visible:e,onCancel:s,afterSubmit:a})=>{let r=(0,n.useRouter)(),{profile:g}=(0,d.useProfile)(),{data:f}=(0,c.useSelectedProjectQuery)(),x=f?.ref??"default",y=(0,o.useMemo)(()=>{let{its:e,ite:t,isHelper:s,helperText:a}=r.query,n=new URLSearchParams;e&&"string"==typeof e&&n.set("its",e),t&&"string"==typeof t&&n.set("ite",t),s&&"string"==typeof s&&n.set("isHelper",s),a&&"string"==typeof a&&n.set("helperText",a);let o=n.toString();return o?`?${o}`:""},[r.query]),{mutate:b,isPending:j}=(0,l.useContentUpsertMutation)({onSuccess:(e,t)=>{i.toast.success("Successfully created new report");let s=t.payload.id;r.push(`/project/${x}/observability/${s}${y}`),a()},onError:e=>{i.toast.error(`Failed to create report: ${e.message}`)}});async function v({name:e,description:t}){return x?g?void b({projectRef:x,payload:{id:(0,u.uuidv4)(),type:"report",name:e,description:t||"",visibility:"project",owner_id:g?.id,content:{schema_version:1,period_start:{time_period:"7d",date:""},period_end:{time_period:"today",date:""},interval:"1d",layout:[]}}}):console.error("Profile is required"):console.error("Project ref is required")}return(0,t.jsx)(h.Modal,{visible:e,onCancel:s,hideFooter:!0,header:"Create a custom report",size:"small",children:(0,t.jsx)(p.Form,{onReset:s,validateOnBlur:!0,initialValues:{name:"",description:""},validate:e=>{let t={};return e.name||(t.name="Required"),t},onSubmit:e=>v(e),children:()=>(0,t.jsxs)(t.Fragment,{children:[(0,t.jsxs)(h.Modal.Content,{className:"space-y-4",children:[(0,t.jsx)(_.Input,{label:"Name",id:"name",name:"name"}),(0,t.jsx)(_.Input.TextArea,{label:"Description",id:"description",placeholder:"Describe your custom report",size:"medium",textAreaClassName:"resize-none"})]}),(0,t.jsx)(h.Modal.Separator,{}),(0,t.jsxs)(h.Modal.Content,{className:"flex items-center justify-end gap-2",children:[(0,t.jsx)(m.Button,{htmlType:"reset",type:"default",onClick:s,disabled:j,children:"Cancel"}),(0,t.jsx)(m.Button,{htmlType:"submit",loading:j,disabled:j,children:"Create report"})]})]})})})};e.s(["CreateReportModal",0,g],303213);let f=({selectedReport:e,initialValues:s,onCancel:a})=>{let{ref:n}=(0,r.useParams)(),{mutate:o,isPending:c}=(0,l.useContentUpsertMutation)({onSuccess:()=>{i.toast.success("Successfully updated report"),a()},onError:e=>{i.toast.error(`Failed to update report: ${e.message}`)}});return(0,t.jsx)(h.Modal,{visible:void 0!==e,onCancel:a,hideFooter:!0,header:"Update custom report",size:"small",children:(0,t.jsx)(p.Form,{onReset:a,validateOnBlur:!0,initialValues:s,validate:function(e){let t={};return e.name||(t.name="This field is required"),t},onSubmit:t=>n?e&&e.id?void(e.project_id&&o({projectRef:n,payload:{...e,owner_id:e.owner_id,project_id:e.project_id,id:e.id,name:t.name,description:t.description||""}})):void 0:console.error("Project ref is required"),children:()=>(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(h.Modal.Content,{children:(0,t.jsx)(_.Input,{label:"Name",id:"name",name:"name"})}),(0,t.jsx)(h.Modal.Content,{children:(0,t.jsx)(_.Input.TextArea,{label:"Description",id:"description",placeholder:"Describe your custom report",size:"medium",textAreaClassName:"resize-none"})}),(0,t.jsx)(h.Modal.Separator,{}),(0,t.jsxs)(h.Modal.Content,{className:"flex items-center justify-end gap-2",children:[(0,t.jsx)(m.Button,{htmlType:"reset",type:"default",onClick:a,disabled:c,children:"Cancel"}),(0,t.jsx)(m.Button,{htmlType:"submit",loading:c,disabled:c,children:"Save custom report"})]})]})})})};var x=e.i(215312),y=e.i(586011),b=e.i(738927),j=e.i(2579),v=e.i(912793),S=e.i(10429),E=e.i(479232),q=e.i(385467),A=e.i(208661),w=e.i(843778),R=e.i(862326),T=e.i(498377),N=e.i(466472),k=e.i(108151),I=e.i(582391),C=e.i(211570),D=e.i(471998),P=e.i(874311);let O=({item:e,pageKey:a,onSelectEdit:r,onSelectDelete:n})=>{let{profile:o}=(0,d.useProfile)(),{can:i}=(0,j.useAsyncCheckPermissions)(s.PermissionAction.UPDATE,"user_content",{resource:{type:"report",visibility:e.report.visibility,owner_id:e.report.owner_id},subject:{id:o?.id}});return(0,t.jsxs)(q.default,{className:(0,w.cn)("pr-2 h-7 pl-3 mt-1 text-foreground-light group-hover:text-foreground/80 text-sm","flex items-center justify-between rounded-md group relative",e.key===a?"bg-surface-300 text-foreground":"hover:text-foreground"),href:e.url,children:[(0,t.jsx)("div",{children:e.name}),i&&(0,t.jsxs)(P.DropdownMenu,{children:[(0,t.jsx)(P.DropdownMenuTrigger,{asChild:!0,children:(0,t.jsx)(m.Button,{type:"text",className:"px-1 opacity-50 hover:opacity-100",icon:(0,t.jsx)(D.MoreVertical,{size:12,strokeWidth:2}),onClick:e=>{e.preventDefault(),e.stopPropagation()}})}),(0,t.jsxs)(P.DropdownMenuContent,{align:"start",className:"w-32 *:gap-x-2",children:[(0,t.jsxs)(P.DropdownMenuItem,{onClick:t=>{t.preventDefault(),t.stopPropagation(),e.id&&r()},children:[(0,t.jsx)(I.Edit2,{size:12}),(0,t.jsx)("div",{children:"Rename report"})]}),(0,t.jsx)(P.DropdownMenuSeparator,{}),(0,t.jsxs)(P.DropdownMenuItem,{onClick:t=>{t.preventDefault(),t.stopPropagation(),e.id&&n()},children:[(0,t.jsx)(C.Trash,{size:12}),(0,t.jsx)("div",{children:"Delete report"})]})]})]})]},e.key+"-menukey")};var L=e.i(242882),$=e.i(714403),M=e.i(837508),F=e.i(246230);async function B({projectRef:e,connectionString:t}){let{result:s}=await (0,$.executeSql)({projectRef:e,connectionString:t,sql:"SELECT current_setting('shared_preload_libraries', true) AS libraries"});return(s[0]?.libraries??"").split(",").some(e=>"supamonitor"===e.trim())}e.s(["default",0,()=>{let e=(0,n.useRouter)(),{profile:l}=(0,d.useProfile)(),{ref:u,id:m}=(0,r.useParams)(),p=m||e.pathname.split("/")[4]||"observability",_=(0,a.useFlag)("observabilityOverview"),{isSupamonitorEnabled:h}=function(){let{data:e}=(0,c.useSelectedProjectQuery)(),{data:t,isLoading:s}=(({projectRef:e,connectionString:t},{enabled:s=!0,...a}={})=>{let{data:r}=(0,c.useSelectedProjectQuery)(),n=r?.status===M.PROJECT_STATUS.ACTIVE_HEALTHY;return(0,L.useQuery)({queryKey:F.databaseKeys.supamonitorEnabled(e),queryFn:()=>B({projectRef:e,connectionString:t}),enabled:s&&void 0!==e&&n,...a})})({projectRef:e?.ref,connectionString:e?.connectionString});return{isSupamonitorEnabled:t??!1,isLoading:s}}(),I=(0,v.useIsFeatureEnabled)("project_storage:all"),{can:C}=(0,j.useAsyncCheckPermissions)(s.PermissionAction.CREATE,"user_content",{resource:{type:"report",owner_id:l?.id},subject:{id:l?.id}}),D=(0,o.useMemo)(()=>{let{its:t,ite:s,isHelper:a,helperText:r}=e.query,n=new URLSearchParams;t&&"string"==typeof t&&n.set("its",t),s&&"string"==typeof s&&n.set("ite",s),a&&"string"==typeof a&&n.set("isHelper",a),r&&"string"==typeof r&&n.set("helperText",r);let o=n.toString();return o?`?${o}`:""},[e.query]),{data:P,isPending:$}=(0,b.useContentQuery)({projectRef:u,type:"report"}),{mutate:U,isPending:H}=(0,y.useContentDeleteMutation)({onSuccess:()=>{Q(!1),i.toast.success("Successfully deleted report"),e.push(`/project/${u}/observability`)},onError:e=>{i.toast.error(`Failed to delete report: ${e.message}`)}}),[Y,Q]=(0,o.useState)(!1),[G,z]=(0,A.useQueryState)("newReport",A.parseAsBoolean.withDefault(!1).withOptions({history:"push",clearOnDefault:!0})),[W,K]=(0,o.useState)(),[V,X]=(0,o.useState)();function J(e){return"report"===e.type}let Z=function(){if(!P)return[];let e=P?.content.filter(J);return(e?.sort((e,t)=>e.name<t.name?-1:+(e.name>t.name))).map((e,t)=>({id:e.id,name:e.name,description:e.description||"",key:e.id||t+"-report",url:`/project/${u}/observability/${e.id}${D}`,hasDropdownActions:!0,report:e}))}(),ee=function(e){let{ref:t,preservedQueryParams:s,showOverview:a,isSupamonitorEnabled:r,storageSupported:n,isPlatform:o=S.IS_PLATFORM}=e,i=[...a?[{name:"Overview",key:"observability",url:`/project/${t}/observability${s}`}]:[],...r?[{name:"Query Insights",key:"query-insights",url:`/project/${t}/observability/query-insights${s}`}]:[{name:"Query Performance",key:"query-performance",url:`/project/${t}/observability/query-performance${s}`}],...o?[{name:"API Gateway",key:"api-overview",url:`/project/${t}/observability/api-overview${s}`}]:[]],l=[{name:"Database",key:"database",url:`/project/${t}/observability/database${s}`},{name:"Data API",key:"postgrest",url:`/project/${t}/observability/postgrest${s}`},{name:"Auth",key:"auth",url:`/project/${t}/observability/auth${s}`},{name:"Edge Functions",key:"edge-functions",url:`/project/${t}/observability/edge-functions${s}`},...n?[{name:"Storage",key:"storage",url:`/project/${t}/observability/storage${s}`}]:[],{name:"Realtime",key:"realtime",url:`/project/${t}/observability/realtime${s}`}],c=[{title:"GENERAL",key:"general-section",items:i}];return o&&c.push({title:"PRODUCT",key:"product-section",items:l}),c}({ref:u,preservedQueryParams:D,showOverview:_,isSupamonitorEnabled:h,storageSupported:I,isPlatform:S.IS_PLATFORM});return(0,t.jsx)(R.Menu,{type:"pills",className:"mt-6",children:$?(0,t.jsxs)("div",{className:"px-5 my-4 space-y-2",children:[(0,t.jsx)(k.ShimmeringLoader,{}),(0,t.jsx)(k.ShimmeringLoader,{className:"w-3/4"}),(0,t.jsx)(k.ShimmeringLoader,{className:"w-1/2"})]}):(0,t.jsxs)("div",{className:"flex flex-col gap-y-6",children:[ee.map((e,s)=>(0,t.jsxs)(o.Fragment,{children:[(0,t.jsx)("div",{className:"h-px w-full bg-border-overlay first:hidden"}),(0,t.jsx)("div",{children:e.items&&e.items.length>0?(0,t.jsxs)("div",{className:"px-2",children:[(0,t.jsx)(R.Menu.Group,{title:(0,t.jsx)("span",{className:"uppercase font-mono",children:e.title})}),(0,t.jsx)("div",{className:"flex flex-col",children:e.items.map(e=>(0,t.jsx)("li",{className:(0,w.cn)("pr-2 mt-1 text-foreground-light group-hover:text-foreground/80 text-sm","flex items-center justify-between rounded-md group relative",e.key===p?"bg-surface-300 text-foreground":"hover:text-foreground"),children:(0,t.jsx)(q.default,{href:e.url,className:"flex-grow h-7 flex justify-between items-center pl-3",children:(0,t.jsx)("span",{children:e.name})})},e.key))},e.key)]}):null})]},s)),S.IS_PLATFORM&&(0,t.jsxs)(o.Fragment,{children:[(0,t.jsx)("div",{className:"h-px w-full bg-border-overlay"}),(0,t.jsxs)("div",{className:"mx-2",children:[(0,t.jsx)(R.Menu.Group,{title:(0,t.jsxs)("span",{className:"flex w-full items-center justify-between relative h-6",children:[(0,t.jsx)("span",{className:"uppercase font-mono",children:"Custom Reports"}),Z.length>0&&(0,t.jsx)(x.ButtonTooltip,{type:"default",size:"tiny",icon:(0,t.jsx)(E.Plus,{}),disabled:!C,className:"flex items-center justify-center h-6 w-6 absolute top-0 -right-1",onClick:()=>{z(!0)},tooltip:{content:{side:"bottom",text:C?void 0:"You need additional permissions to create custom reports"}}})]})}),0===Z.length?(0,t.jsx)("div",{className:"px-2",children:(0,t.jsx)(T.InnerSideBarEmptyPanel,{title:"No custom reports yet",description:"Create and save custom reports to track your project metrics",actions:(0,t.jsx)(x.ButtonTooltip,{type:"default",icon:(0,t.jsx)(E.Plus,{}),disabled:!C,onClick:()=>{z(!0)},tooltip:{content:{side:"bottom",text:C?void 0:"You need additional permissions to create custom reports"}},children:"New custom report"})})}):(0,t.jsx)(t.Fragment,{children:Z.map(e=>(0,t.jsx)(O,{item:e,pageKey:p,onSelectEdit:()=>{X(e.report)},onSelectDelete:()=>{K(e.report),Q(!0)}},e.id))})]})]}),(0,t.jsx)(f,{onCancel:()=>X(void 0),selectedReport:V,initialValues:{name:V?.name||"",description:V?.description||""}}),(0,t.jsx)(N.default,{title:"Delete custom report",confirmLabel:"Delete report",confirmLabelLoading:"Deleting report",size:"medium",loading:H,visible:Y,onCancel:()=>Q(!1),onConfirm:()=>void 0===u?console.error("Project ref is required"):W?.id===void 0?console.error("Report ID is required"):void U({projectRef:u,ids:[W.id]}),children:(0,t.jsx)("div",{className:"text-sm text-foreground-light grid gap-4",children:(0,t.jsx)("div",{className:"grid gap-1",children:(0,t.jsxs)("p",{children:["Are you sure you want to delete '",W?.name,"'?"]})})})}),(0,t.jsx)(g,{visible:G,onCancel:()=>z(!1),afterSubmit:()=>z(!1)})]})})}],256337)},212846,e=>{"use strict";var t=e.i(478902);e.i(128328);var s=e.i(86086),a=e.i(947748),r=e.i(158639),n=e.i(888525);e.i(69870);var o=e.i(284399),i=e.i(124416),l=e.i(967052),c=e.i(924115),u=e.i(670447),d=e.i(470754);let m=()=>{let e=(0,l.useTrack)(),{ref:s}=(0,r.useParams)(),{dismissBanner:n}=(0,d.useBannerStack)(),[,m]=(0,i.useLocalStorageQuery)(a.LOCAL_STORAGE_KEYS.INDEX_ADVISOR_NOTICE_DISMISSED(s??""),!1);return(0,t.jsx)(u.BannerCard,{onDismiss:()=>{m(!0),n("index-advisor-banner"),e("index_advisor_banner_dismiss_button_clicked")},children:(0,t.jsxs)("div",{className:"flex flex-col gap-y-4",children:[(0,t.jsx)("div",{className:"flex flex-col gap-y-2 items-start",children:(0,t.jsx)("div",{className:"p-2 rounded-lg bg-warning-300 text-warning",children:(0,t.jsx)(c.Lightbulb,{size:16})})}),(0,t.jsxs)("div",{className:"flex flex-col gap-y-1 mb-2",children:[(0,t.jsx)("p",{className:"text-sm font-medium",children:"Enable Index Advisor"}),(0,t.jsx)("p",{className:"text-xs text-foreground-lighter text-balance",children:"Recommends indexes to improve query performance."})]}),(0,t.jsx)("div",{className:"flex gap-2",children:(0,t.jsx)(o.EnableIndexAdvisorButton,{})})]})})};var p=e.i(587433),_=e.i(223173),h=e.i(389959),g=e.i(837710),f=e.i(385467),x=e.i(10429);let y=()=>{let{ref:e}=(0,r.useParams)(),s=(0,l.useTrack)(),{dismissBanner:n}=(0,d.useBannerStack)(),[,o]=(0,i.useLocalStorageQuery)(a.LOCAL_STORAGE_KEYS.OBSERVABILITY_BANNER_DISMISSED(e??""),!1);return(0,t.jsx)(u.BannerCard,{onDismiss:()=>{o(!0),n("metrics-api-banner"),s("metrics_api_banner_dismiss_button_clicked")},children:(0,t.jsxs)("div",{className:"flex flex-col gap-y-4",children:[(0,t.jsxs)("div",{className:"flex flex-col gap-y-2 items-start",children:[(0,t.jsx)(p.Badge,{variant:"success",className:"-ml-0.5 uppercase inline-flex items-center mb-2",children:"Beta"}),(0,t.jsx)("div",{className:"flex items-center gap-4",children:_.LOG_DRAIN_TYPES.filter(e=>"sentry"!==e.value).map(e=>(0,t.jsx)(h.default.Fragment,{children:h.default.cloneElement(e.icon,{height:20,width:20})},e.value))})]}),(0,t.jsxs)("div",{className:"flex flex-col gap-y-1 mb-2",children:[(0,t.jsx)("p",{className:"text-sm font-medium",children:"Export Metrics to your dashboards"}),(0,t.jsx)("p",{className:"text-xs text-foreground-lighter text-balance",children:"Visualize over 200 database performance and health metrics with our Metrics API."})]}),(0,t.jsx)("div",{className:"flex gap-2",children:(0,t.jsx)(g.Button,{type:"default",size:"tiny",asChild:!0,children:(0,t.jsx)(f.default,{href:`${x.DOCS_URL}/guides/telemetry/metrics`,target:"_blank",onClick:()=>s("metrics_api_banner_cta_button_clicked"),children:"Get started for free"})})})]})})};var b=e.i(902780),j=e.i(912793),v=e.i(951138),S=e.i(514228),E=e.i(825713),q=e.i(256337);let A=({title:e,children:o})=>{let{ref:l}=(0,r.useParams)(),c=(0,S.usePathname)(),{addBanner:u,dismissBanner:p}=(0,d.useBannerStack)(),{isIndexAdvisorAvailable:_,isIndexAdvisorEnabled:g}=(0,n.useIndexAdvisorStatus)(),[f]=(0,i.useLocalStorageQuery)(a.LOCAL_STORAGE_KEYS.OBSERVABILITY_BANNER_DISMISSED(l??""),!1),[x]=(0,i.useLocalStorageQuery)(a.LOCAL_STORAGE_KEYS.INDEX_ADVISOR_NOTICE_DISMISSED(l??""),!1);(0,h.useEffect)(()=>{!f&&s.IS_PLATFORM?u({id:"metrics-api-banner",isDismissed:!1,content:(0,t.jsx)(y,{}),priority:1}):p("metrics-api-banner")},[f,u,p]);let v=(0,h.useRef)(c);(0,h.useEffect)(()=>{let e=c?.includes("/query-performance");e&&_&&!g&&!x?u({id:"index-advisor-banner",isDismissed:!1,content:(0,t.jsx)(m,{}),priority:3}):(x||!e||g)&&p("index-advisor-banner"),v.current=c},[c,_,g,x,u,p]);let{reportsAll:A}=(0,j.useIsFeatureEnabled)(["reports:all"]);return A?(0,t.jsx)(E.ProjectLayout,{product:"Observability",browserTitle:{section:e},productMenu:(0,t.jsx)(q.default,{}),isBlocking:!1,children:o}):(0,t.jsx)(b.UnknownInterface,{urlBack:`/project/${l}`})},w=(0,v.withAuth)(e=>{let{ref:s}=(0,r.useParams)(),{reportsAll:a}=(0,j.useIsFeatureEnabled)(["reports:all"]);return a?(0,t.jsx)(A,{...e}):(0,t.jsx)(b.UnknownInterface,{urlBack:`/project/${s}`})});e.s(["default",0,w],212846)}]);

//# debugId=7e44b0f9-0538-9684-f9ef-cad7b271713a
//# sourceMappingURL=4e32a3d873827b9c.js.map