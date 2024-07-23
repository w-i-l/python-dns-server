<h1>Python DNS Server</h1>
<h2>An implementation from scratch of a fully functional authoritive and recursive DNS server </h2>
<img src="https://github.com/user-attachments/assets/c0f2e385-bb81-4be9-8e1b-a44015b1e89a">



<br>
<hr>
<h2>About it</h2>
<p>This project was made as a demonstration on how a DNS server would work. It doesn't contain a caching mechanism or any advance feature, besides serving responses for basic DNS queries.

The server is capable of handling both authoritive and recursive queries. The authoritive queries are handled by the server itself, while the recursive queries are forwarded to a Google DNS server (8.8.8.8) and the response is then forwarded back to the client.

Before moving on, I want to clarify all the capabilities of this server and its limitations.
</p>

<table>
    <th>Multithreading</th>
    <th>Authoritive queries</th>
    <th>Recursive queries</th>
    <th>Cache</th>
    <th>Supported DNS over HTTPS</th>
    <th>Supported DNS over TLS</th>
    <tr>
        <td>No</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>No</td>
        <td>No</td>
        <td>No</td>
    </tr>
</table>

<table>
    <th>Multiple questions in one query</th>
    <th>Truncated answer</th>
    <th>Assignable IP address</th>
    <th>Tunneling detection</th>
    <th>Domain name compression</th>
    <th>Pointer compression</th>
    <tr>
        <td>No</td>
        <td>No</td>
        <td>Yes</td>
        <td>No</td>
        <td>Yes</td>
        <td>No</td>
    </tr>
</table>

<table>
    <th>Supported record types</th>
    <th>Supported classes</th>
    <th>Supported query types</th>
    <th>Supported response types</th>
    <th>Supported response codes</th>
    <tr>
        <td>
            <ul>
                <li>A</li>
                <li>CNAME</li>
                <li>MX</li>
                <li>NS</li>
                <li>SOA</li>
                <li>TXT</li>
             </ul>
        </td>
        <td>
            <ul>
                <li>IN</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>A</li>
                <li>CNAME</li>
                <li>MX</li>
                <li>NS</li>
                <li>SOA</li>
                <li>TXT</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>A</li>
                <li>CNAME</li>
                <li>MX</li>
                <li>NS</li>
                <li>SOA</li>
                <li>TXT</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>NAME_ERROR</li>
                <li>NO_ERROR</li>
                <li>FORMAT_ERROR</li>
                <li>SERVER_FAILURE</li>
                <li>NOT_IMPLEMENTED</li>
                <li>REFUSED</li>
            </ul>
        </td>
    </tr>
</table>

>**Note**: The following code will contain explanation for a Unix based system. For Windows, the commands might be different, please consider that when running the server.

<br>
<hr>
<h2>How to use it</h2>
<p>By default the server is made to run on port 53, which is the default port for DNS servers. In order to this program tu run, you would need root permissions to run the server. You can use the following command:</p>

```bash
sudo python3 main.py
```

<p>The server is configured to use the loopback address which should be <code>127.0.0.1</code>. If you want to change the address, you can do so by changing the <code>DNS_SERVER_IP</code> variable in the <code>main.py</code> file before running the command from above.</p>

<p>The server records are kept in the <code>zones</code> folder. These are not formatted as a normal DNS zone file, but as a JSON file, for more flexibility and ease of use. The server will load all the records from the <code>zones</code> folder and will use them to respond to queries. If you want to add a new record, you can do so by adding a new JSON file in the <code>zones</code> folder. The JSON file should respect the same format use in the examples provided.</p>

<p>For adding a new zone file for a new website called <code>mySite.com</code>, you can create a new JSON file called <code>mySite.com.zone</code> in the <code>zones</code> folder with the following content:</p>

```json
{
    "name": "mySite.com",
    "ttl": 3600,
    "soa": {
        "name": "@",
        "ttl": 3600,
        "minimum": 3600,
        "refresh": 3600,
        "retry": 1800,
        "expire": 1209600,
        "serial": 2024051501,
        "mname": "ns1.mySite.com.",
        "rname": "admin.mySite.com."
    }       
}
```

>**Note**: The server will read those files only on starting the application. If you want to add a new record, you would need to restart the server.

<p>For testing the server, you can use the <a href="https://linux.die.net/man/1/dig">dig</a> command. The <code>dig</code> command is a DNS lookup utility that can be used to query the DNS server. You can use the following command to query the server:</p>

```bash
dig example.com @127.0.0.1 txt
```

<p>If you want to query the server for a recursive query, jsut try with a domain that is not in the <code>zones</code> folder. The server will forward the query to the Google DNS server and will return the response to you.</p>

<br>
<hr>
<h2>How it works</h2>
<p>The server tries to lookup for the query in the <code>zones</code> folder. If the query is found, the server will respond with the records found in the JSON file. If the query is not found, the server will forward the query to the Google DNS server and will return the response to the client.</p>

<p>The process is split across multiple classes, each with its own responsibility. The <code>main.py</code> file is the entry point of the application. It will start the server and will listen for incoming requests. The <code>dns_question.py</code> file contains the <code>DNSQuestion</code> class which is used to parse the incoming query. The <code>dns_answear.py</code> file contains the <code>DNSAnswear</code> class which is used to create the response for the query.</p>

<br>
<hr>
<h2>Tech specs</h2>

<p>For creating and handle the DNS fields I created the <code>dns_enums.py</code> file which contains all the supported fields for the DNS protocol.</p>

<p>The <code>dns_errors.py</code> file contains the Python errors that can be raised by the server which are further translated into DNS response codes.</p>

<p>All the functions have been documented so that you can understand what each function does and how it works. The code is also commented so that you can understand the logic behind each function.</p>

<br>
<hr>
<h2>Brief explanation</h2>

<ul>
   <li><a href="https://www.youtube.com/watch?v=UVR9lhUGAyU">DNS from Fireship</a></li>
    <li><a href="https://www.youtube.com/watch?v=27r4Bzuj5NQ">ByteByteGo's video</a></li>
</ul>

<br>
<hr>
<h2>Further reading</h2>

<ul>
<li><a href="https://datatracker.ietf.org/doc/html/rfc1035">DOMAIN NAMES - IMPLEMENTATION AND SPECIFICATION</a></li>
<li><a href="https://www.cloudflare.com/en-gb/learning/dns/what-is-dns/">Cloudflare explanation</a></li>
<li><a href="https://www.youtube.com/watch?v=HdrPWGZ3NRo&list=PLBOh8f9FoHHhvO5e5HF_6mYvtZegobYX2">DNS tutorial in Python</a></li>
</ul>
