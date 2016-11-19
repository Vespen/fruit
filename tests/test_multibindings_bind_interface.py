#!/usr/bin/env python3
#  Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from nose2.tools import params

from fruit_test_common import *
from fruit_test_config import CXX_COMPILER_NAME
import unittest
import re

COMMON_DEFINITIONS = '''
#include <fruit/fruit.h>
#include <vector>
#include "test_macros.h"

struct Annotation {};
struct Annotation1 {};
struct Annotation2 {};
'''

@params(
    ('X', 'int'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation2, int>'))
def test_error_not_base(XAnnot, intAnnot):
    expect_compile_error(
    'NotABaseClassOfError<X,int>',
    'I is not a base class of C.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<> getComponent() {
  return fruit::createComponent()
    .addMultibinding<XAnnot, intAnnot>();
}
''',
    locals())

@params(
    ('Scaler', 'ScalerImpl'),
    ('fruit::Annotated<Annotation1, Scaler>', 'fruit::Annotated<Annotation2, ScalerImpl>'))
def test_error_abstract_class(ScalerAnnot, ScalerImplAnnot):
    expect_compile_error(
    'NoBindingFoundForAbstractClassError<ScalerImpl>',
    'No explicit binding was found for C, and C is an abstract class',
    COMMON_DEFINITIONS + '''
struct Scaler {
  virtual double scale(double x) = 0;
};

struct ScalerImpl : public Scaler {
  // Note: here we "forgot" to implement scale() (on purpose, for this test) so ScalerImpl is an abstract class.
};

fruit::Component<> getComponent() {
  return fruit::createComponent()
    .addMultibinding<ScalerAnnot, ScalerImplAnnot>();
}
''',
    locals())

@params(
    ('Scaler', 'ScalerImpl'),
    ('fruit::Annotated<Annotation1, Scaler>', 'fruit::Annotated<Annotation2, ScalerImpl>'))
@unittest.skipUnless(
    re.search('Clang', CXX_COMPILER_NAME) is not None,
    'This is Clang-only because GCC >=4.9 refuses to even mention the type C() when C is an abstract class, '
    'while Clang allows to mention the type (but of course there can be no functions with this type)')
def test_error_abstract_class_clang(ScalerAnnot, ScalerImplAnnot):
    expect_compile_error(
    'CannotConstructAbstractClassError<ScalerImpl>',
    'The specified class can.t be constructed because it.s an abstract class.',
    COMMON_DEFINITIONS + '''
struct Scaler {
  virtual double scale(double x) = 0;
};

struct ScalerImpl : public Scaler {
  INJECT(ScalerImpl()) = default;

  // Note: here we "forgot" to implement scale() (on purpose, for this test) so ScalerImpl is an abstract class.
};

fruit::Component<> getComponent() {
  return fruit::createComponent()
    .addMultibinding<ScalerAnnot, ScalerImplAnnot>();
}
''',
    locals())

if __name__ == '__main__':
    import nose2
    nose2.main()
