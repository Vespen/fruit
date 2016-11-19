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

from fruit_test_common import *
from nose2.tools.params import params

COMMON_DEFINITIONS = '''
#include <fruit/fruit.h>
#include <vector>
#include "test_macros.h"

struct Annotation1 {};
struct Annotation2 {};
'''

@params('X','fruit::Annotated<Annotation1, X>')
def test_error_already_bound(XAnnot):
    expect_compile_error(
    'TypeAlreadyBoundError<XAnnot>',
    'Trying to bind C but it is already bound.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<XAnnot> getComponent() {
  static X x;
  return fruit::createComponent()
    .registerConstructor<XAnnot()>()
    .bindInstance<XAnnot, X>(x);
}
''',
    locals())

def test_already_bound_with_different_annotation_ok():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {};

using XAnnot1 = fruit::Annotated<Annotation1, X>;
using XAnnot2 = fruit::Annotated<Annotation2, X>;

fruit::Component<XAnnot1, XAnnot2> getComponent() {
  static X x;
  return fruit::createComponent()
    .registerConstructor<XAnnot1()>()
    .bindInstance<XAnnot2>(x);
}

int main() {
  fruit::Injector<XAnnot1, XAnnot2> injector(getComponent());
  injector.get<XAnnot1>();
  injector.get<XAnnot2>();
}
''')

if __name__ == '__main__':
    import nose2
    nose2.main()
