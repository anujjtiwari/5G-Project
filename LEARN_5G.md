# Learn 5G with the 5G Core Explorer: a course from zero

This course assumes you know nothing about 5G. Work through it with the explorer open next to it
(double-click `tools/understand_5g/index.html`). Every lesson tells you which **message number** to look
at. Use the chapter buttons at the bottom, or the **← →** arrow keys, until the counter shows that number.

> Shortcut: in the browser's address bar, add `?step=24&tab=flow` to the end of the explorer's address
> and press Enter. It opens message 24 in the Call flow tab.

How to study:

1. Read a lesson here.
2. Open the matching messages in the explorer and look at the map, the state panel and the decode.
3. Explain it out loud as if you were teaching someone. If you get stuck, re-read that part.

There are 17 short lessons (0–16). Allow 4–6 hours in total. Lessons 0–3 matter most; everything else builds on them.

---

## Lesson 0: What 5G actually is (the big picture)

### The one-sentence version

A mobile network is a system that gets a phone connected to the internet, wirelessly, securely, while it
moves, and with the right quality for each app. 5G is the fifth generation of that system.

### The two halves

Every mobile network has two big parts:

| Part | Name | Job | Everyday analogy |
|---|---|---|---|
| The radio part | **RAN** (Radio Access Network) | Carries data through the air between the phone and a base station (the tower). | The roads and toll booths near your house |
| The brain part | **Core network** (in 5G: **5GC**, the 5G Core) | Decides who you are, whether you may connect, what IP address you get, what quality you get, and where your data goes. | The government offices and motorway control centre behind the scenes |

**Your original project (the RAN digital twin) is all about the first half**: towers, radio
signals, coverage and scheduling. **The 5G Core Explorer explains the second half and how the two halves work
together.** That's why it lives behind a button in your twin. Together they cover the whole 5G
system, end to end.

### Two kinds of traffic: control plane and user plane

This is the most important idea in all of mobile networking, so it's worth slowing down here.

- **User plane (UP)**: your actual data, such as the YouTube video, the WhatsApp message, the web page.
- **Control plane (CP)**: signalling, meaning the network's own conversations about you. "Who is this phone?",
  "Is this subscriber allowed?", "Give them IP address 10.45.0.7", "They moved to another tower".

Analogy: on a train, the passengers and luggage are the user plane. The station announcements, tickets,
signals and timetables are the control plane. You need both, but they are very different things.

In the explorer's **Network map**, the tick boxes "Control plane" and "User plane" switch these two
on and off. Try it now: untick "Control plane" and only the data path is left: **UE → gNB → UPF → DN**.
That short path is the whole route your YouTube video takes. Everything else on the map is the control
plane, the "brain".

### Why 5G is special (what to say when someone asks "what's new in 5G?")

1. **Faster and wider radio.** More bandwidth (your twin uses 100 MHz at 3.5 GHz), flexible "numerology" and
   massive antennas with beamforming.
2. **Service-Based Architecture (SBA).** The core is no longer boxes wired with special telecom
   protocols. It's a set of software services that talk to each other with web APIs (HTTP/2 + JSON),
   like modern cloud apps. You can see this as the horizontal **"SBI bus"** on the map.
3. **Control/user plane separation (CUPS).** The "brain" (SMF) and the "muscle" (UPF) are separate, so
   UPFs can be placed close to users at the edge (low latency).
4. **Network slicing.** One physical network can act as several virtual networks: one for phones
   (eMBB), one for factory robots (URLLC), one for sensors (mMTC).
5. **Fine-grained QoS.** Each app flow can get its own quality (the "5QI").
6. **Better privacy and security.** Your permanent ID is never sent in clear text (SUCI), and the
   home network confirms authentication.

Remember these six. Each one appears somewhere in the explorer.

---

## Lesson 1: Meet the cast (every box on the map)

Open the **Network map** tab. Each box is a **Network Function (NF)**, a piece of software with
one job. Click each box as you read; the right panel shows the same details.

### The radio side (left of the map)

**UE (User Equipment)**: the phone. Inside it is the **USIM** (the SIM card). The USIM holds two secrets:
- **SUPI**: your permanent subscriber ID (like an IMSI: `imsi-001010000000001`). Think of it as your passport number.
- **K**: a secret key shared only with your home operator. It never leaves the SIM, and it is never sent anywhere.

**gNB (5G base station)**: the "g" means 5G; "NB" means NodeB, the old name for a base station. It is the tower plus
the computer that runs it. There are two on the map (gNB-1 and gNB-2) so we can show a handover. In real
networks a gNB is often split into **RU** (radio unit on the mast), **DU** (fast real-time processing)
and **CU** (higher-layer processing).
- *Connection to your twin:* your twin models exactly these gNBs: where they are, which way they point,
  how strong their signal is everywhere, and how they schedule users.

### The core: control-plane functions (the "brain")

| NF | Full name | One-line job | Analogy |
|---|---|---|---|
| **AMF** | Access and Mobility Management Function | The phone's single point of contact in the core: registration, security, tracking where the phone is | Immigration desk at the airport |
| **SMF** | Session Management Function | Sets up "sessions" (internet connections): gives IP address, picks a UPF, programs it | Travel agent who books your route |
| **AUSF** | Authentication Server Function | Runs the "are you really who you say?" check | Passport verification office |
| **UDM** | Unified Data Management | Holds subscriber records and generates the security challenge | The citizen registry |
| **UDR** | Unified Data Repository | The actual database behind UDM and PCF | Filing cabinet |
| **PCF** | Policy Control Function | Decides the rules: speed limits, quality levels, charging | The rule book |
| **NRF** | Network Repository Function | Directory of all NFs: "where is an SMF?" | Phone book |
| **NSSF** | Network Slice Selection Function | Picks which network slice a phone may use | The lane-assignment desk |
| **NEF** | Network Exposure Function | Safe gateway for outside apps to ask the network for things | Embassy |
| **AF** | Application Function | An outside app server (e.g. a video-call service) | A company booking priority boarding |

### The core: user-plane function (the "muscle")

**UPF (User Plane Function)**: every single packet of your data passes through here. It follows rules
installed by the SMF: forward, buffer, rate-limit, count bytes for billing.

**DN (Data Network)**: the destination, usually the internet. Its name is the **DNN**, e.g. `internet`.

### The memory trick

> **AMF = Access & Mobility (who and where). SMF = Session (connection). UPF = User data.**
> **AUSF + UDM = Identity and security. PCF = Policy. NRF = Directory.**

If you can explain those three lines, you understand 80% of the 5G core.

---

## Lesson 2: The lines (interfaces) and the languages (protocols)

The lines between boxes are **interfaces**. Each has a name, and each uses a **protocol** (a "language").
Click the small grey labels on the map (Uu, N2, N3…) to see the details on the right.

| Interface | Between | Carries | Protocol (language) | Colour in explorer |
|---|---|---|---|---|
| **Uu** | Phone ↔ gNB | Everything over the air | RRC for control, PHY/MAC for radio | yellow (RRC), grey (PHY) |
| **N1** | Phone ↔ AMF | Phone's own messages to the core | **NAS** | orange (5GMM), pink (5GSM) |
| **N2** | gNB ↔ AMF | Control between tower and core | **NGAP** | blue |
| **N3** | gNB ↔ UPF | User data, tunnelled | **GTP-U** | lime (user data) |
| **N4** | SMF ↔ UPF | Rules from brain to muscle | **PFCP** | green |
| **N6** | UPF ↔ Internet | Plain internet traffic | IP | lime |
| **Xn** | gNB ↔ gNB | Handover between towers | **XnAP** | purple |
| **SBI** | Between all core NFs | Service requests | **HTTP/2 + JSON** (web APIs) | cyan |
| **N33** | AF ↔ NEF | Outside apps asking for features | HTTP/2 REST | cyan |

### The trickiest idea here: N1 is "logical"

On the map, N1 is a **dashed curved line** from the phone straight to the AMF. But there's no cable or
radio directly between them. NAS messages physically travel **phone → (inside RRC) → gNB → (inside NGAP) → AMF**.
The gNB carries them like a sealed envelope without opening them.

Analogy: you send a sealed letter to the immigration office (AMF) through a courier (gNB). The courier
handles the envelope but cannot read the letter. In the explorer, NAS messages show a **"carried in:"** box,
for example "NGAP DownlinkNASTransport → RRC DLInformationTransfer". That is the envelope inside the envelope.

### Protocol stacks

When you click an interface, you see a **stack** of layers. Read it top to bottom: each layer wraps the one above.
Example, N3:

```
User IP packet                    ← your actual data
GTP-U (+ QFI)                     ← tunnel label: "this belongs to session X, quality flow 1"
UDP (port 2152)
IP (transport)                    ← the operator's own network addresses
Data link / Physical              ← cables
```

Analogy: your letter (data) goes into an envelope with a tracking number (GTP-U TEID), which goes
into a truck (IP) on a road (physical).

### The radio stack (Uu), explained once

| Layer | Job (simple) |
|---|---|
| **SDAP** | Sorts packets into quality lanes (QoS flow → radio bearer) |
| **PDCP** | Encrypts, protects integrity, compresses headers |
| **RLC** | Splits and reassembles, re-sends lost pieces |
| **MAC** | Scheduling and fast retransmission (HARQ): who sends when |
| **PHY** | Turns bits into radio waves: modulation, coding, antennas |
| **RRC** | (control) Manages the radio connection: setup, security, handover |

**Your twin works mostly at the PHY/MAC level**: signal strength, SINR and scheduling.

---

## Lesson 3: The state panel, the phone's "status"

Look at **UE & session state** on the right of the map. These values change as messages flow, and changed
values flash yellow. Learn these and you can explain any procedure.

| Field | Meaning | Possible values |
|---|---|---|
| **RRC** | Is the phone's *radio* connected to a tower? | `RRC_IDLE` (asleep), `RRC_CONNECTED` (active). 5G also has `RRC_INACTIVE` (light sleep). |
| **RM** (Registration Management) | Does the core *know and accept* this phone? | `RM-DEREGISTERED`, `RM-REGISTERED` |
| **CM** (Connection Management) | Is there an active signalling link between phone and AMF right now? | `CM-IDLE`, `CM-CONNECTED` |
| **Serving cell / PCI** | Which tower and cell the phone uses | PCI 101 (gNB-1), PCI 205 (gNB-2) |
| **C-RNTI** | The phone's short "seat number" inside a cell while connected | e.g. `0x4601` |
| **Identity (core)** | What the core knows the phone as | SUCI (hidden) → SUPI (real) |
| **5G-GUTI** | A temporary nickname used instead of the real ID | `5G-GUTI 001-01-…-C0FFEE01` |
| **Security** | Is encryption on? | NAS (phone↔AMF) and AS (phone↔gNB) |
| **PDU session** | Is there an internet connection? | session 1, DNN internet, slice SST 1 |
| **UE IP** | The phone's IP address | `10.45.0.7` |
| **QoS flows** | Quality lanes | QFI 1 / 5QI 9 (best effort), later QFI 2 / 5QI 2 (video, guaranteed) |
| **N3 TEIDs** | Tunnel IDs for uplink and downlink between gNB and UPF | `0x00000A01`, `0x0000B7A2` |

**Key insight to teach:** a phone can be **RM-REGISTERED but CM-IDLE / RRC_IDLE**. That's your phone in
your pocket right now: the network knows you, you have an IP address, but the radio is asleep to save battery.
When someone messages you, the network **pages** you (Lesson 8).

---

## Lesson 4: Chapter 0 (Network start-up, messages 1–6)

Before any phone appears, the network has to build itself. Click the **Start-up** chapter button.

| # | Message | What's happening | Why it matters |
|---|---|---|---|
| 1 | `Nnrf_NFManagement_NFRegister` (AMF → NRF) | The AMF tells the directory "I exist, here is my address, here are my services". Every NF does this. | This is how service-based architecture works: NFs find each other through the NRF, like microservices in the cloud. |
| 2–3 | `PFCP Association Setup` (SMF ↔ UPF) | The brain and muscle shake hands. | CUPS: the SMF can now program this UPF. |
| 4–5 | `NG Setup` (gNB ↔ AMF) | The tower connects to the core and says which areas (TAC) and slices it serves. | Without this, no phone can register through this tower. |
| 6 | `Xn Setup` (gNB-1 ↔ gNB-2) | Neighbour towers introduce themselves. | Enables fast handovers later. |

**Explorer exercise:** open message 1 in the **Call flow** tab and look at the decode. Notice `nfType: AMF`,
`sNssais: [{sst:1}]` (the slice it serves) and `heartBeatTimer: 60 s` (it must say "I'm still alive"
every minute).

**Teaching line:** *"Before any phone can connect, every core function registers in a directory, the
brain pairs with the data-forwarding engine, and towers connect to the core."*

---

## Lesson 5: Chapter 1 (Cell search & RRC connection, messages 7–13)

The phone is switched on. It knows nothing. It needs to find a tower and get a radio connection.

### 7. SSB burst: "Is anyone there?"
The tower constantly broadcasts **SSBs** (Synchronisation Signal Blocks) in up to 8 beams, like a lighthouse
sweeping. The phone listens and finds:
- **PSS + SSS** → the cell's ID: **PCI = 3 × N_ID1 + N_ID2 = 3 × 33 + 2 = 101**.
- Signal strength of each beam: **RSRP** (here −86 dBm). Picks the strongest beam (SSB 3).

*Connection to your twin:* the **RSRP coverage map** in your 3D viewer predicts exactly this number
at every point on campus. This is the clearest link between your twin and the explorer.

### 8. MIB (Master Information Block)
A tiny broadcast message, 23 bits. It gives the frame number and where to find the next message (SIB1).

### 9. SIB1 (System Information Block 1)
The tower's "notice board": network ID (PLMN 001/01), tracking area code, the minimum signal needed
(−124 dBm), and how to do random access. The phone checks the **S-criterion**:
`measured − minimum = −86 − (−124) = 38 dB > 0` → good enough, so the phone **camps** on this cell.

### 10–13. Random access: four messages to get a seat
| # | Msg | Simple explanation |
|---|---|---|
| 10 | **Msg1, PRACH preamble** | Phone raises its hand: sends one of 64 random "codes". |
| 11 | **Msg2, Random Access Response** | Tower says "I hear you. Shift your timing by this much (Timing Advance), here's permission to talk, and here's a temporary ID." TA = 12 means the phone is about 470 m away. |
| 12 | **Msg3, RRCSetupRequest** | Phone says "I'd like a connection, reason: I want to register (mo-Signalling)". |
| 13 | **Msg4, RRCSetup** | Tower echoes the phone's ID (so if two phones picked the same code, only one wins: *contention resolution*) and sets up the first signalling channel, **SRB1**. |

State change: **RRC_IDLE → RRC_CONNECTED**, C-RNTI = 0x4601.

**Teaching line:** *"The phone listens to the tower's beacons, reads its notice board, raises its hand, gets
a timing correction, and receives a dedicated radio connection."*

---

## Lesson 6: Chapter 2 (Registration & security, messages 14–33)

This is the most important chapter. Take your time. Goal: the network learns who the phone is, both sides
prove they are genuine, encryption turns on, and the phone gets a temporary ID.

### Part A: The phone introduces itself (14–15)
- **14 RRCSetupComplete [Registration Request]**: inside it is the NAS message "Registration Request".
  The phone does *not* send its real ID (SUPI). It sends a **SUCI**: its ID **encrypted with the home
  network's public key**. Anyone listening to the air learns nothing.
  *(This is new in 5G. In 4G the IMSI could sometimes be sent in clear text, which made "IMSI catchers" possible.)*
- **15 Initial UE Message**: the gNB chooses an AMF and forwards the sealed NAS envelope, adding the
  location (cell and tracking area). The phone is now **CM-CONNECTED**.

### Part B: Authentication, 5G-AKA (16–23)
5G-AKA means "Authentication and Key Agreement". The core idea:

> Both the SIM and the home network know the secret key **K**. Neither ever sends it.
> Instead the network sends a random **challenge**, the SIM computes an **answer** using K, and the network checks it.
> At the same time, the SIM checks that the challenge really came from the home network (mutual authentication).

The flow:
1. **16** AMF → AUSF: "please authenticate this SUCI".
2. **17** AUSF → UDM: "generate a challenge". The UDM's **SIDF** decrypts SUCI → SUPI. Its **ARPF** uses K to make:
   - **RAND**: random challenge
   - **AUTN**: proof that the network knows K (so the SIM can detect fake towers)
   - **XRES\***: expected answer
   - **KAUSF**: a key
3. **18** UDM → AUSF: here's the vector + the real SUPI.
4. **19** AUSF → AMF: gives RAND, AUTN and only a **hash** of the expected answer (HXRES\*). The visited network
   can check the answer but cannot fake success: the home network keeps the final say.
5. **20** AMF → phone: **Authentication Request** (RAND, AUTN).
6. **21** Phone → AMF: SIM checks AUTN (is the network real?), computes **RES\*** and sends it.
7. **22** AMF checks the hash, then forwards RES\* to the AUSF.
8. **23** AUSF: RES\* = XRES\* → **AUTHENTICATION_SUCCESS**. Gives the AMF the SUPI and the anchor key **KSEAF**.

**Key hierarchy** (say it like a family tree): **K → KAUSF → KSEAF → KAMF → KgNB → radio keys**.
Each level is derived from the one above, so a key leaked at a lower level doesn't expose the higher ones.

### Part C: Turning on encryption (24–25, 28–30)
- **24 Security Mode Command (NAS)**: AMF picks algorithms (**NEA2** = encryption, **NIA2** = integrity, both AES-based).
  It also *replays* the phone's own capabilities back so the phone can detect if an attacker downgraded them.
- **25 Security Mode Complete**: from now on all NAS messages are encrypted.
- **28 Initial Context Setup Request**: AMF gives the gNB the key **KgNB**.
- **29–30 RRC SecurityModeCommand/Complete**: radio-level encryption turns on.

Two layers of security: **NAS security** (phone ↔ AMF) and **AS security** (phone ↔ gNB).

### Part D: Getting the subscription and finishing (26–27, 31–33)
- **26** AMF → UDM: "I'm now serving this phone" (UECM Registration) + "what is this subscriber allowed?"
  (SDM: speed limit 2 Gbps down / 1 Gbps up, slice SST 1).
- **27** AMF → PCF: access policy.
- **31 RRCReconfiguration [Registration Accept]**: the phone receives its **5G-GUTI** (temporary ID), the list of
  tracking areas it can roam in without re-registering, and **measurement settings** (used later for handover).
- **33 Registration Complete**: **RM-REGISTERED**. 

**Teaching line:** *"The phone sends a hidden ID. The home network issues a challenge only the real SIM can
answer, and the SIM checks the network is genuine too. Both sides derive keys, encryption is switched on,
and the phone gets a temporary nickname."*

---

## Lesson 7: Chapter 3 (PDU session: getting on the internet, messages 34–50)

Registered ≠ online. A **PDU session** is the actual internet connection: an IP address, a quality level
and a data path through a UPF.

### The request (34–39)
- **34** Phone → AMF: "PDU Session Establishment Request: session ID 1, to DNN `internet`, slice SST 1, IPv4".
  Note the colour: **pink = 5GSM** (session management). The AMF just forwards it to an SMF.
- **35–36** AMF asks the **NRF** "which SMF serves `internet` on slice 1?" This is SBA in action.
- **37** AMF → SMF: `CreateSMContext`.
- **38** SMF → UDM: session subscription (default quality 5QI 9, session speed limit).
- **39** SMF → AMF: "OK, context created".

### The policy (40)
- **40** SMF → PCF: PCF decides **5QI 9** (best-effort internet), **Session-AMBR** 1 Gbps down / 500 Mbps up.

### Programming the UPF (41–42), the CUPS moment
The SMF installs rules in the UPF over **N4 (PFCP)**:
- **PDR** (Packet Detection Rule): "how to recognise packets". Uplink: by tunnel ID; downlink: by UE IP 10.45.0.7.
- **FAR** (Forwarding Action Rule): "what to do". Uplink → forward to internet. Downlink → **BUFFER** (because we don't yet know the tower's tunnel ID).
- **QER** (QoS Enforcement Rule): speed limits.
- **URR** (Usage Reporting Rule): count bytes for billing.

Memory trick: **PDR = "if"**, **FAR = "then"**, **QER = "how fast"**, **URR = "how much"**.

The UPF replies (**42**) with its **uplink TEID** `0x00000A01`. TEID = Tunnel Endpoint ID, the tunnel's "door number".

### Telling the RAN and the phone (43–47)
- **43** SMF → AMF (`N1N2MessageTransfer`): two envelopes. **N2** for the gNB (tunnel info + quality profile),
  **N1** for the phone (Accept: your IP is 10.45.0.7, your quality rules).
- **44** AMF → gNB: PDU Session Resource Setup Request.
- **45** gNB → phone: **RRCReconfiguration** creates **DRB1** (Data Radio Bearer, the radio "lane" for data),
  maps QoS flow 1 onto it, and delivers the Accept. **The phone now has an IP address.**
- **46** Phone confirms.
- **47** gNB → AMF: here's my **downlink TEID** `0x0000B7A2`.

### Closing the loop (48–50)
- **48–49** AMF → SMF → UPF: change the downlink FAR from BUFFER to **FORWARD to gNB tunnel 0x0000B7A2**.
- **50** Done. **User plane ACTIVE.**

**Teaching line:** *"The phone asks for an internet session. The SMF gets the policy from the PCF, programs the
UPF with packet rules, and both ends of a GTP tunnel exchange IDs. The radio creates a data lane and the phone
gets its IP address."*

**Draw this on a board.** It's the picture to remember:
```
Phone ──(DRB1, encrypted radio)── gNB ══(GTP tunnel, TEID)══ UPF ──(plain IP)── Internet
```

---

## Lesson 8: Chapter 4 (User data & scheduling, messages 51–54)

This is where the core meets **your RAN twin**.

- **51 Uplink packet**: open the decode and you'll see the packet at every layer:
  - Inner IP: `10.45.0.7 → 203.0.113.10:443` (an HTTPS request). This never changes end to end.
  - On the radio: SDAP (QFI 1) → PDCP (encrypted) → RLC → MAC → PHY.
  - On N3: wrapped in GTP-U with TEID `0x00000A01`.
  - At the UPF: rule matched → tunnel removed → sent to the internet.
- **52 Downlink packet**: the reverse. UPF matches UE IP → wraps in tunnel to the gNB → gNB puts it in DRB1's queue →
  **the scheduler decides when it goes out**.
- **53 CSI report**: the phone measures the channel and reports **CQI** (Channel Quality Indicator, 1–15).
  CQI 11 = 64QAM, about 5.1 bits per resource element.
- **54 DCI + PDSCH**: every slot (0.5 ms at 30 kHz), the gNB **scheduler** chooses which user gets which
  **PRBs** (Physical Resource Blocks) and which **MCS** (modulation and coding). The phone replies ACK/NACK (**HARQ**).

### Now open the **Air interface** tab
This is the radio math your twin uses (`dt/kpi.py`):

```
SINR  →  CQI  →  modulation + code rate  →  bits per resource element  →  throughput
```
- Move the **SINR** slider. Watch CQI change, the constellation dots spread when SINR drops, and throughput fall.
- **Constellation**: yellow = perfect points, blue = what's received with noise. When blue clouds overlap,
  the receiver confuses symbols, so the scheduler must use a simpler modulation (lower CQI).
- **Throughput formula** (memorise this, professors ask about it):
  ```
  throughput = layers × PRBs × 12 subcarriers × 14 symbols × slots per second
               × bits per RE × (1 − overhead 14%) × (1 − BLER 10%)  ÷  users sharing
  ```
  Example at CQI 15, 273 PRB, 30 kHz, 1 layer ≈ **526 Mbps**.
- **Numerology μ**: subcarrier spacing = 15 × 2^μ kHz. Larger μ → shorter slots → lower latency, but fewer PRBs per MHz.
  μ = 1 (30 kHz, 0.5 ms slot) is standard at 3.5 GHz.
- **Frame**: 10 ms frame → 10 subframes of 1 ms → 2^μ slots → 14 OFDM symbols each.

**Teaching line:** *"Everything upstream sets up the path. The actual speed you get is decided here, every
half-millisecond, by the gNB scheduler, based on your SINR. That is what my RAN digital twin models and improves:
B1 is the baseline, T3 is channel-aware scheduling."*

---

## Lesson 9: Chapter 5 (QoS on demand & network exposure, messages 55–62)

Scenario: a video-call app wants **guaranteed** speed for its video.

### First, what is QoS in 5G?
- A **QoS flow** is a quality lane, identified by **QFI** (QoS Flow Identifier).
- Each flow has a **5QI** (5G QoS Identifier) pointing to standard characteristics:

| 5QI | Type | Example | Delay budget |
|---|---|---|---|
| 1 | GBR (guaranteed) | Voice call | 100 ms |
| 2 | GBR | Conversational video | 150 ms |
| 9 | Non-GBR (best effort) | Internet browsing (default) | 300 ms |
| 82+ | Delay-critical GBR | Factory automation (URLLC) | 10 ms or less |

- **GBR** = the network reserves a guaranteed bit rate. **Non-GBR** = best effort.

### The flow
- **55** AF → NEF: the app server asks "give UE 10.45.0.7's video flow (UDP ports 50000–50100) the video QoS profile".
  External apps never get internal IDs; the NEF protects the network.
- **56** NEF → PCF: policy authorisation request.
- **57** PCF → SMF: new rule. **5QI 2, guaranteed 6 Mbps**.
- **58** SMF → UPF: new PDR that catches video packets and marks them **QFI 2**, with a QER enforcing 6 Mbps.
- **59–60** SMF → AMF → gNB: add QoS flow 2. The gNB does **admission control** ("can I guarantee 6 Mbps?").
- **61** gNB → phone: creates **DRB2** for QFI 2.
- **62** Phone confirms.

Now the state shows **two lanes**: QFI 1 (internet, best effort) and QFI 2 (video, guaranteed).

### Network slicing (explain it with this chapter)
A **slice** is a whole virtual network, identified by **S-NSSAI** = **SST** (type: 1 = eMBB, 2 = URLLC,
3 = mMTC/IoT) + optional SD. Slicing uses the same building blocks you just saw (selection by the NSSF,
policy by the PCF, dedicated SMF/UPF and radio resources), just at a bigger scale. Everything in this demo uses
**SST 1 (eMBB)**.

**Teaching line:** *"Apps can ask the network for quality through the NEF. The PCF turns that into a rule,
the SMF programs the UPF and the radio, and a new guaranteed lane appears alongside the best-effort one."*

---

## Lesson 10: Chapter 6 (Xn handover, messages 63–73)

You walk from gNB-1 to gNB-2. **Watch the UE box slide down the map.**

1. **63 MeasurementReport (event A3)**: the phone was told (in message 31) to report when a neighbour is
   **3 dB stronger** than the current cell for **160 ms**. gNB-2 = −88 dBm, gNB-1 = −95 dBm, so the condition is met.
   *Your twin's mobility walks (Task 5) count exactly these serving-cell changes.*
2. **64 Handover Request** (gNB-1 → gNB-2 over **Xn**): "here's this phone's full context: keys, sessions, quality flows".
3. **65 Acknowledge**: gNB-2 accepts, reserves a **dedicated preamble** (no contention) and a new C-RNTI.
4. **66 RRCReconfiguration (handover command)**: phone is told to jump to PCI 205. Short interruption starts.
5. **67 SN Status Transfer + data forwarding**: gNB-1 forwards buffered packets to gNB-2 so **nothing is lost**.
6. **68 RACH + RRCReconfigurationComplete**: phone arrives at gNB-2. Uplink works immediately.
7. **69 Path Switch Request** (gNB-2 → AMF): "send downlink traffic to me now, my TEID is 0x0000C113".
8. **70–71** AMF → SMF → UPF: switch the downlink tunnel. UPF sends an **End Marker** on the old path ("no more packets coming that way").
9. **72 Path Switch Ack**: AMF gives fresh keys (forward security: gNB-1 can't compute future keys).
10. **73 UE Context Release**: gNB-1 forgets the phone.

**What did NOT change:** IP address, PDU session, QoS flows. The UPF is the **anchor**, which is why your
video call doesn't drop when you move.

**Teaching line:** *"The towers prepare the handover between themselves, the phone jumps, buffered data is forwarded,
and only then is the core asked to move the tunnel. The IP address stays the same because the UPF anchors the session."*

---

## Lesson 11: Chapter 7 (Idle mode, paging & service request, messages 74–87)

### Going to sleep (74–78)
- No traffic for a while → gNB asks to release (**74**, cause: user-inactivity).
- SMF tells UPF: **buffer downlink and notify me** (**76**).
- **78 RRCRelease** → phone goes **RRC_IDLE / CM-IDLE**, but is **still RM-REGISTERED** with the same IP.
- It wakes every **1.28 s** (DRX paging cycle) for a few milliseconds to check if it's being called.

### Someone sends a message (79–87)
1. **79** A chat message arrives at the UPF → buffered.
2. **80** UPF → SMF: "downlink data waiting" (PFCP Session Report).
3. **81** SMF → AMF: "please reach this UE". AMF answers "trying" (202).
4. **82 Paging** (AMF → gNBs): the AMF only knows the **tracking area**, not the exact cell, so it pages **all** towers in the area.
5. **83** The towers broadcast the phone's **5G-S-TMSI** at its paging occasion.
6. **84 Service Request**: the phone does random access again and asks to resume. **No re-authentication**: it reuses its keys.
7. **85–86** Context restored, UPF switched back to forward.
8. **87** The chat message is delivered. Total delay is roughly 100–300 ms, mostly waiting for the paging occasion.

**Teaching line:** *"Idle mode is how phones last all day. The network keeps your registration and IP, buffers
incoming data, pages you across the tracking area, and you wake up with a quick Service Request. Battery life
and latency trade off through the paging cycle."*

---

## Lesson 12: Chapter 8 (Deregistration, messages 88–93)

Airplane mode:
- **88** Deregistration Request.
- **89–90** SMF releases the session; UPF deletes rules and returns the **final usage report** (bytes used, which is how billing works).
- **91** AMF deregisters from the UDM.
- **92** Deregistration Accept → **RM-DEREGISTERED**.
- **93** Radio released. Everything is back to where chapter 1 started.

---

## Lesson 13: The other tabs, explained

### SBI API builder
Shows the **real web API calls** between core NFs. Each one has:
- **Method + path**, e.g. `POST /nausf-auth/v1/ue-authentications`
- **JSON body**, which you can edit with the inputs at the top (SUPI, DNN, slice, 5QI…)
- **Response**, e.g. `201 Created`
- "Copy as curl" gives you a command-line version.

**Why it matters:** this is what "cloud-native 5G core" means. Core functions are web services. Real open-source
cores (**Open5GS**, **free5GC**) expose these exact endpoints. Good demo: change SST from 1 to 2 (URLLC) and
show how the slice changes in every request.

### Glossary
55 terms. Use the filter box. The top search bar searches **everything**: NFs, interfaces, messages and even
individual fields inside messages (try typing `TEID` or `5qi`).

---

## Lesson 14: How the program itself is built (if someone asks)

| File | What it contains |
|---|---|
| `tools/understand_5g/index.html` | Page layout and styling (the "skeleton") |
| `tools/understand_5g/data.js` | **All the 5G knowledge**: network functions, interfaces, the 93 messages with their decoded fields, API examples and glossary. To change any text or add a message, edit this file. |
| `tools/understand_5g/app.js` | The behaviour: drawing the map, animating messages, the sequence chart, decodes, search, the radio calculator. |
| `tools/install_5g_explorer.py` | Copies the explorer next to the 3D twin and adds the "Understand 5G" button. |

How it works internally, in plain words:
- Every message in `data.js` has: **from**, **to**, **protocol**, **interface**, **name**, **narration**,
  **decoded fields** and **state changes**.
- The app replays the state changes in order, so the state panel is always correct for any message number.
- For the animation, it finds the path between the two boxes through the real links (e.g. NAS from phone to AMF
  goes via the gNB; core-to-core goes via the SBI bus).
- It's pure HTML + JavaScript, so it runs offline in any browser with no install.

---

## Lesson 15: How to present it (10-minute demo script)

1. **(1 min) Why.** "My project is a digital twin of the 5G radio network. But the radio is only half of 5G.
   I built this explorer so anyone can see the whole system, end to end." Open the twin → click **Understand 5G**.
2. **(1 min) The map.** Untick control plane: "this is the data path". Tick it back: "this is the brain".
   Click AMF, SMF, UPF and give the one-liners.
3. **(2 min) Registration.** Jump to the Registration chapter, press ▶. Pause at message 14 (hidden ID / SUCI),
   20–21 (challenge-response), 24 (encryption on). Point at the state panel changing.
4. **(2 min) PDU session.** Show message 41 decode (PDR/FAR rules) and message 45 (IP address arrives).
   Draw "phone – gNB – tunnel – UPF – internet".
5. **(2 min) Link to my twin.** Message 53 (CQI) → **Air interface** tab, move SINR slider: "this is exactly
   the model my twin uses to compute throughput for every user on campus."
6. **(1 min) Handover.** Press ▶ from message 63 and watch the UE move: "my twin's mobility study counts these".
7. **(1 min) API builder.** "The core is web services. Here's the real HTTP request for authentication."

---

## Lesson 16: Questions you will be asked (with answers)

**Q: What's the difference between AMF and SMF?**
AMF handles the *phone* (registration, security, mobility). SMF handles *sessions* (IP address, UPF, QoS). One AMF per phone; possibly several SMFs, one per session.

**Q: Why is the UPF separate from the SMF?**
CUPS. Control and data scale differently. UPFs can be put near users (edge computing) for low latency, while the SMF stays central.

**Q: How does 5G protect my identity?**
The SUPI is never sent over the air. The phone sends a SUCI (encrypted with the home network's public key), and afterwards uses a temporary 5G-GUTI.

**Q: What's the difference between RRC_IDLE and CM-IDLE and RM-DEREGISTERED?**
RRC = radio link to the tower. CM = signalling link to the AMF. RM = whether the network has registered you at all. Idle phones are usually RM-REGISTERED + CM-IDLE + RRC_IDLE.

**Q: What is a TEID?**
Tunnel Endpoint Identifier: a 32-bit number identifying one end of a GTP-U tunnel. Each receiver chooses its own TEID (UPF picks the uplink one, gNB picks the downlink one).

**Q: Why does the IP not change during handover?**
The UPF is the anchor. Only the tunnel between UPF and gNB moves (path switch).

**Q: What's a 5QI?**
A number that points to standard QoS characteristics (guaranteed or not, priority, delay budget, error rate). 9 = default internet, 1 = voice, 2 = video.

**Q: What's network slicing?**
Multiple virtual networks on one physical network, identified by S-NSSAI (SST + SD). Example: eMBB for phones, URLLC for robots, mMTC for sensors.

**Q: Is this a real 5G core?**
No. It's a teaching simulation. The message flows and field names follow the 3GPP standards (Release 16/17), but it doesn't send real packets, and identities are illustrative (test network 001/01). Real open-source cores like Open5GS + UERANSIM could be connected as future work.

**Q: How does this relate to your digital twin?**
The twin models the gNBs and the radio link: coverage (RSRP), SINR, cell selection, scheduling and mobility. The explorer shows the full procedures around those parts. The Air interface tab uses the same SINR→CQI→throughput model as the twin.

---

## Self-test (answers below; don't peek)

1. Name the three NFs on the data path from phone to internet.
2. Which NF would you blame if the phone gets no IP address?
3. In which message does the phone first get its 5G-GUTI?
4. What does a FAR with "BUFF" mean, and when is it used? (two situations)
5. What is the difference between N1 and N2?
6. Why does the AUSF give the AMF HXRES\* instead of XRES\*?
7. After handover, which TEID changes: uplink, downlink, or both?
8. A phone has SINR 0 dB. Roughly what CQI and modulation? (Use the Air interface tab.)
9. What triggers paging?
10. What is the difference between QFI and 5QI?

<details><summary>Answers</summary>

1. gNB, UPF (plus the DN as the destination); the UE is the start.
2. SMF (it allocates the IP and sets up the session), or the UPF if the rules failed.
3. Message 31, RRCReconfiguration carrying Registration Accept (confirmed by Registration Complete, 33).
4. "Buffer packets." Used during session setup before the gNB's downlink TEID is known (message 41), and in idle mode while the phone sleeps (message 76).
5. N1 is phone ↔ AMF (NAS, logical). N2 is gNB ↔ AMF (NGAP, physical, and it carries the N1 messages inside).
6. So the visited/serving network can check the answer but can't fake a successful authentication; the home network keeps the final decision.
7. Only the downlink TEID (the UPF now sends to gNB-2's TEID). The uplink TEID at the UPF stays the same.
8. CQI 2, QPSK (about 0.38 bit per resource element).
9. Downlink data arrives at the UPF for a phone in CM-IDLE. The UPF tells the SMF, which tells the AMF, which pages.
10. QFI is the label on packets identifying the flow (a local ID). 5QI is the standard QoS class that flow gets (its characteristics).
</details>

---

## Where to go deeper (optional)

- 3GPP **TS 23.501** (architecture) and **TS 23.502** (procedures) are the official sources for everything in the explorer.
- **TS 24.501** (NAS messages), **TS 38.331** (RRC), **TS 38.413** (NGAP), **TS 29.244** (PFCP), **TS 33.501** (security).
- To see a real core: install **Open5GS** (core) + **UERANSIM** (simulated phone and gNB) on Linux and capture traffic with **Wireshark**. You'll see the same message names as in the explorer.
