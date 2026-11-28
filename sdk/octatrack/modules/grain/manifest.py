"""GRAIN -- a track machine: a granular engine on the track's Flex sample, six grains at a time.

The engine is based on Model-TG's granular mode (TinyGregAudio, MIT) and extended: random pan per grain, a SYNC mode,
DIR as a share of backward grains, a SCAN read head, POS in fine steps. Stock's FLEX reader runs a neutral note (PTCH 0,
RATE forward, no retrig or stretch) so the voice stays live; the machine's render replaces the source PCM in the frame
packet with up to six windowed grains read from the Flex sample in stock's pages, before the DSP takes it. The engine
applies the pitch itself. A page with the waveform and the grains is drawn over SRC, and a full-screen page over the
third press of PLAYBACK.

No stock code is patched: the machine joins the base's machine list and START dispatch through runtime.json
(ot_machines, ot_machine_starts) and draws through module_draw. Everything GRAIN keeps in a Part passes stock's own
power-on check. The connection to stock follows AMIGA (Jannik Assfalg, MIT).
"""

from remix.schema import Category, Detour, Gate, Kind, Linked, Module, Proof
from remix.stock_guard import stock_guard

MODULE = Module(
    name="grain",
    key="GRAIN",
    kind=Kind.CF_PATCH,
    category=Category.MACHINES,
    author="AForceTrulyEvil",
    author_url="https://github.com/AForceTrulyEvil",
    proof=Proof.HARDWARE,
    proof_note="Host tests cover this engine. The author played an earlier build on an MKI (TESTING.md).",
    doc="Track machine: six-grain granular on the Flex sample, with a waveform view and a full-screen page.",
    linked=(
        Linked("grain", "modules/grain/grain_core.s", cpu="5475", dram=True),
    ),
    detours=(
        Detour(0x400041C4, stock_guard(0x400041C4, 8, "935fcfbfbcb323efa9fe7bada6974a125a8ea86989b79c535d556fc72d4d138d"),
               "grain", "grain_copy", "Skip the FLEX reader's PCM copy while Grain renders its own", pad_to=8),
    ),
    gates=(Gate("modules/grain/test_grain.py", remix_arg=False),),
)
