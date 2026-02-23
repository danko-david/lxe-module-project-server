#!/bin/bash

export PROJECT_SERVER_DNS_CORE_ZONE_NAME='{{ HOST_DNS_NAME }}'

page()
{
cat << EOF
Content-type: text/html

<!doctype html>
<html lang="hu">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Service discovery</title>
	<style>
:root {
    --primary: #4CAF50;
    --primary-dark: #388E3C;
    --bg-color: #f4f7f6;
    --text-color: #333;
    --card-bg: #ffffff;
}
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
header {
    background-color: var(--primary);
    padding: 1rem 2rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
header a {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}
content {
    flex: 1;
    padding: 2rem;
    max-width: 1200px;
    margin: 20px auto;
    background: var(--card-bg);
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    width: 90%;
    display: block;
    overflow: scroll;
    overflow: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
}
table th {
    background-color: var(--primary);
    color: white;
    padding: 15px;
    text-align: left;
}
table td {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
}
table tr:hover {
    background-color: #f9f9f9;
}
	</style>
</head>
<body>
	<header>
		<a href="/">Service discovery on ${PROJECT_SERVER_DNS_CORE_ZONE_NAME}</a>
	</header>
	<content>
		$(create_table)
	</content>
</body>
</html>
}
EOF
}

tr()
{
	X=${X:-td}
	echo "<tr>"
	for I in "$@"
	do
		echo "<$X>$I</$X>"
	done
	echo "</tr>"
}

{% raw %}

create_table()
{
echo '<h1>List of containers</h1><table>'
	X=th tr "Stack" "Container Name" "DNS Name" "IP" "Ports"

	docker ps -q | xargs -n 1 docker inspect --format $'{{ index .Config.Labels "com.docker.compose.service" }}\t{{.Name}}\t{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\t{{range $k,$v := .NetworkSettings.Ports }}{{if $v }}{{ index (index $v 0 ) "HostPort" }}->{{$k}} {{end}}{{end}}' | grep -vP '^\s+' \
		| while IFS=$'\t' read -a data
		do
			hn="${data[1]/\//}.${data[0]}.${PROJECT_SERVER_DNS_CORE_ZONE_NAME}"
			tr "${data[0]}" "${data[1]/\//}" "${hn}" "${data[2]}" "${data[3]}" "${data[4]}"
		done
echo '</table>'
}

{% endraw %}

page
