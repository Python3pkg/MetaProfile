import os
import sys
import numpy as np
from pandas import DataFrame
import matplotlib.gridspec as gridspec
import pylab as pl
import seaborn as sns
from Bio import SeqIO, Seq, motifs
from Bio.Alphabet import IUPAC
import HTSeq

from Signal import Signal
from Profile import Profile
from Window import Window


class WrongFiletypeException(Exception): pass
class NotSuchAFileException(Exception): pass
class NoSignalsException(Exception): pass
class NoProfilesException(Exception): pass
class NotSuchAProfileException(Exception): pass
class NotSuchAProfileTypeException(Exception): pass

class ProfileCreator():

    """A class that handles creation of the genomic profile"""

    def __init__(self, signals=None, windows=None):
        """Initialize ProfileCreator

        :param signals_path: @todo
        :param signals_filetype: @todo
        :param windows_path: @todo
        :param windows_filetype: @todo
        :param window_length: @todo
        :param pseudocount: @todo

        """
        self.windows = []
        if windows:
            self.add_windows(windows)
        self.signals = []
        if signals:
            self.add_signals(signals)
        self.profiles = {}

    def create_profiles(self, update=False, delete=False):
        """Prepare array of profiles for each each signal. For each window a pseudocount
        is added.
        """
        if update and delete:
            raise Exception("You can chose one of two: delete or update, not both.")
        elif (len(self.profiles.keys()) != 0 and delete):
            self.profiles = {}
            sys.stderr.write("Dictionary with profiles will be deleted and constructed form the scratch!\n")
            if not self.signals:
                raise NoSignalsException("No signals detected. Add some genomic signals before using this function.\n")
            if not self.signals:
                raise NoWindowsException("No windows detected. Add some windows before using this function.\n")
            for signal in self.signals:
                for window in self.windows:
                    profile_name = self.__construct_profile_name(signal, window)
                    if profile_name not in self.profiles:
                        self.profiles[profile_name] = Profile(signal, window)
                    else:
                        raise Exception("Profile %s already in dictionary! You may have duplicated something." % profile_name)
        elif (len(self.profiles.keys()) != 0 and update):
            sys.stderr.write("Dictionary with profiles will be updated!\n")
            if not self.signals:
                raise NoSignalsException("No signals detected. Add some genomic signals before using this function.\n")
            if not self.signals:
                raise NoWindowsException("No windows detected. Add some windows before using this function.\n")
            for signal in self.signals:
                for window in self.windows:
                    profile_name = self.__construct_profile_name(signal, window)
                    if profile_name not in self.profiles:
                        self.profiles[profile_name] = Profile(signal, window)
                    else:
                        sys.stderr.write("Profile %s already in dictionary! Skipping.\n" % profile_name)
        elif (len(self.profiles.keys()) != 0 and not update) or (len(self.profiles.keys()) != 0 and not delete):
            sys.stderr.write("Dictionary with profiles is not empty. Use update=True to force updating the profile or delete=True to construct it from scratch!\n")
        else:
            assert len(self.profiles.keys()) == 0
            if not self.signals:
                raise NoSignalsException("No signals detected. Add some genomic signals before using this function.\n")
            if not self.signals:
                raise NoWindowsException("No windows detected. Add some windows before using this function.\n")
            for signal in self.signals:
                for window in self.windows:
                    profile_name = self.__construct_profile_name(signal, window)
                    if profile_name not in self.profiles:
                        self.profiles[profile_name] = Profile(signal, window)
                    else:
                        raise Exception("Profile %s already in dictionary! You may have duplicated something." % profile_name)




    def add_windows(self, windows):
        """Add a windows to ProfileCreator using

        :param windows: list of Window.Window objects
        """
        window_names = [w.name for w in self.windows]
        if type(windows) != type([]):
            raise Exception("Input should be a list!")
        for window in windows:
            if not isinstance(window, Window):
                raise Exception("input has to be of type Window")
            if window.name in window_names:
                sys.stderr.write("Window %s already in ProfileCreator. Skipping.\n" % window.names)
                continue
            self.windows.append(window)

    def add_signals(self, signals):
        """Add a signals to ProfileCreator using

        :param signals: list of Signal.Signal objects
        """
        signal_names = [s.name for s in self.signals]
        if type(signals) != type([]):
            raise Exception("Input should be a list!")
        for signal in signals:
            if not isinstance(signal, Signal):
                raise Exception("input has to be of type Signal")
            if signal.name in signal_names:
                sys.stderr.write("Signal %s already in ProfileCreator. Skipping.\n" % signal.name)
                continue
            self.signals.append(signal)

    def show_profiles(self):
        """List all profiles available"""
        if len(self.profiles.keys()) == 0:
            sys.stderr.write("No profiles yet.\n")
        for i, profile in enumerate(self.profiles.values()):
            sys.stderr.write("%i. '%s'\n" % (i + 1, profile.name))

    def __construct_profile_name(self, s, w):
        return "%s on %s" % (s.name, w.name)
