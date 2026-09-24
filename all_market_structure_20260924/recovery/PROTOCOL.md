# AMS-001 recovery and demo connectivity

The first acquisition process was interrupted before its final writes. Its console
reported 14,330 series, 25 perps and a capped 5,000 incentives; raw receipts were
not saved. Those counts are not restored evidence. The empty original capture
directory and original frozen source remain untouched.

Recovery imports the original scanner with unchanged selection, parsing and request
rules. Each completed request batch is journaled and each completed catalog is
checkpointed. A new capture directory prevents confusing old and new observations.
A 300-second process deadline may truncate acquisition; partial evidence is retained
and cannot be labeled a complete scan. No automatic retry of the entire study.

Separately test the demo WebSocket with the explicitly supplied Ed25519 credential.
Select the first three tickers lexically from one demo open-markets page (limit 100).
Subscribe to orderbook_delta and trade for these only, for at most 30 seconds or
500 messages. Attempt recommended demo host, then documented legacy demo host only
on connection failure. Record only whitelisted public market message fields and
sanitized error types/status codes. Do not save keys, auth headers, signatures,
account identifiers or client-order identifiers. Credentials enter via stdin into
memory, never through repository files. No order placement, no production auth.

This is an engineering connectivity test, not a profit experiment. A successful
handshake is distinct from subscription acknowledgement, snapshot and delta receipt.
Zero updates means unobserved activity, not a broken feed or proven stable quotes.
Do not score fills, latency advantage or profitability from demo activity.
