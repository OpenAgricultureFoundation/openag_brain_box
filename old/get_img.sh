#!/bin/bash
  fswebcam -r 2592x1944 --no-banner ~/openag_brain_box/img.bmp
  python ~/openag_brain_box/compute_canny.py
