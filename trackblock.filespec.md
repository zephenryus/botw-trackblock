# `trackblock` File Specification

## `trackblock` File Layout

## `trackblock` Header

### Header Layout

### Header Structure

| Offset | Length | Type | Description |
|--:|:-:|---|---|
| `0x00` | 1 | Unsigned Byte | File Index? |
| `0x01` | 1 | Unsigned Byte | File Index Repeated? |
| `0x02` | 1 | Unsigned Byte | Unknown. Values include `2f`, `08`. |
| `0x03` | 1 | Unsigned Byte | Unknown. Always `00` |
| `0x04` | 1 | Unsigned Byte | Unknown. Values include `01` and `00` |
| `0x05` | 1 | Unsigned Byte | Unknown. Values include `2c` and `cd` |
| `0x06` | 2 | Unsigned Short | Unknown. Always `00 00` |
| `0x08` | 4 | Unsigned Int | Unknown. Values include `00 00 00 00` and `00 00 00 10` |
| `0x0c` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x10` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x14` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x18` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x1c` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x20` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x24` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x28` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x2c` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x30` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x34` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x38` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |
| `0x3c` | 4 | Unsigned Int | Unknown. Always `00 00 00 00`. Padding? |

#### Parameters

## `trackblock` Body

Each file covers an average of 7.42 hours (based on 26 files).

### Segments

Segments cover an average of about 10 minutes

#### Segment Header

| Offset | Length | Type | Description |
|--:|:-:|---|---|
| `0x00` | 4 | Unsigned Int | Timestamp1 |
| `0x04` | 4 | Unsigned Int | Timestamp2 |
| `0x08` | 8 | | Padding |

#### Parameters

##### Timestamps

These values are not always equal. Possibly playtime vs playtime + idle time?

## Flags

| Flag | `0` | `1` | Description |
|--:|:-:|:-:|---|
| `0` | -y | +y | Mirrors point across the x-axis |
| `1` | `false` | `true` | Horizontal shift (`+4096`) |
| `2` | -x | +x | Mirrors point across the y-axis |
| `3` | `true` | `false` | Teleport start? |
| `4` | `true` | `false` | Teleport end? |
| `5` | `true` | `false` | Death |
| `6` | `true` | `false` | Riding a horse? |
| `7` | `true` | `false` | `true` = MainField , `false` = Dungeon or AocField |
