# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class MalyanConnectionFixPlugin(octoprint.plugin.OctoPrintPlugin):

	def initialize(self):
		if self._plugin_manager and self._plugin_manager.get_plugin("serial_double_open") is not None:
			self._logger.warn("It looks like the Serial Double Open Plugin is installed. "
			                  "The Malyan/Monoprice Connection Fix Plugin supersedes it. "
			                  "It is strongly recommended to uninstall or disable the Serial Double Open Plugin now.")

	def serial_factory(self, comm_instance, port, baudrate, read_timeout, *args, **kwargs):
		"""
		This is basically the default serial factory, just with a weird open/open/close sequence applied

		Performs

			OPEN Parity.ODD
			OPEN Parity.NONE
			CLOSE Parity.ODD
			USE Parity.NONE

		See https://github.com/foosel/OctoPrint/issues/2271#issuecomment-352662485
		"""
		import serial
		from octoprint.events import Events, eventManager

		if port is None or port == 'AUTO':
			# no known port, try auto detection
			comm_instance._changeState(comm_instance.STATE_DETECT_SERIAL)

			port = comm_instance._detect_port()
			if port is None:
				comm_instance._errorValue = 'Failed to autodetect serial port, please set it manually.'
				comm_instance._changeState(comm_instance.STATE_ERROR)
				eventManager().fire(Events.ERROR, {"error": comm_instance.getErrorString()})
				comm_instance._log("Failed to autodetect serial port, please set it manually.")
				return None

		# Do not try to handle the Virtual Printer with this plugin
		# solves Issue 2 https://github.com/OctoPrint/OctoPrint-MalyanConnectionFix/issues/2
		if port == "VIRTUAL":
			comm_instance._log("Bypassing Malyan/Monoprice Connection Fix Plugin when using Virtual Printer")
			return None

		# connect to regular serial port
		comm_instance._log("Connecting to: %s" % port)
		comm_instance._log("Using Malyan/Monoprice Connection Fix Plugin to create serial connection")
		if baudrate == 0:
			from octoprint.util.comm import baudrateList
			baudrates = baudrateList()
			baudrate = 115200 if 115200 in baudrates else baudrates[0]

		serial_obj1 = serial.Serial(str(port), baudrate, timeout=read_timeout, writeTimeout=10000,
		                            parity=serial.PARITY_ODD)
		serial_obj2 = serial.Serial(str(port), baudrate, timeout=read_timeout, writeTimeout=10000,
		                            parity=serial.PARITY_NONE)

		serial_obj1.close()  # close the first instance, we don't actually need that

		return serial_obj2  # return the second instance

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			malyan_connection_fix=dict(
				displayName="Malyan/Monoprice Connection Fix Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-MalyanConnectionFix",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-MalyanConnectionFix/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Malyan/Monoprice Connection Fix"


def __plugin_check__():
	import sys

	if sys.platform == "win32":
		# Windows doesn't allow double open, log and bail
		import logging
		logging.getLogger("octoprint.plugins.malyan_connection_fix").error("Cannot run this plugin under Windows")
		return False

	return True


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = MalyanConnectionFixPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.transport.serial.factory": __plugin_implementation__.serial_factory,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

