"""Mock data and constants for testing.

This module provides sample data and constants used across tests.
"""

SAMPLE_ALS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Ableton Creator="Ableton Live 11.0.0" MajorVersion="5" MinorVersion="11.0">
    <LiveSet>
        <Tempo>
            <Manual Value="120"/>
        </Tempo>
        <TimeSignature>
            <TimeSignatures>
                <RemoteableTimeSignature>
                    <Numerator Value="4"/>
                    <Denominator Value="4"/>
                </RemoteableTimeSignature>
            </TimeSignatures>
        </TimeSignature>
        <Tracks>
            <AudioTrack Id="0">
                <Name>
                    <EffectiveName Value="1-Audio"/>
                    <UserName Value=""/>
                </Name>
                <ColorIndex Value="5"/>
                <Freeze Value="false"/>
            </AudioTrack>
            <MidiTrack Id="1">
                <Name>
                    <EffectiveName Value="2-MIDI"/>
                    <UserName Value=""/>
                </Name>
                <ColorIndex Value="10"/>
                <Freeze Value="false"/>
            </MidiTrack>
            <ReturnTrack Id="2">
                <Name>
                    <EffectiveName Value="A-Reverb"/>
                    <UserName Value=""/>
                </Name>
            </ReturnTrack>
        </Tracks>
        <FileRef>
            <Path Value="Samples/Kick.wav"/>
        </FileRef>
        <FileRef>
            <Name Value="Snare.wav"/>
        </FileRef>
        <PluginDesc>
            <VstPluginInfo>
                <PlugName Value="Serum"/>
            </VstPluginInfo>
        </PluginDesc>
    </LiveSet>
</Ableton>
"""

MINIMAL_ALS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Ableton Creator="Ableton Live 11.0.0">
    <LiveSet>
        <Tracks/>
    </LiveSet>
</Ableton>
"""

INVALID_XML = """<?xml version="1.0" encoding="UTF-8"?>
<NotAbleton>
    <SomeData/>
</NotAbleton>
"""

# Test constants
DEFAULT_TEST_TEMPO = 120.0
DEFAULT_TEST_TIME_SIGNATURE = (4, 4)
TEST_APP_NAME = "Aelus"
TEST_APP_VERSION = "0.1.0"
