# --------------------------------------------------------------------------
# NifFormat.NiNode
# Custom functions for NiNode.
# --------------------------------------------------------------------------
# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007, NIF File Format Library and Tools.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENCE BLOCK *****
# --------------------------------------------------------------------------

def addChild(self, childblock):
    """Add block to child list."""
    num_children = self.numChildren
    self.numChildren = num_children + 1
    self.children.updateSize()
    self.children[num_children] = childblock

def removeChild(self, childblock):
    """Remove a block from the child list."""
    children = [child for child in self.children if child != childblock]
    self.numChildren = len(children)
    self.children.updateSize()
    for i, child in enumerate(children):
        self.children[i] = child

def flattenTree(self):
    """Reposition all NiNode blocks in the tree to be children of this
    node. For instance, call this on the parent of a skeleton root for
    oblivion creatures."""

    for child in self.children:
        if isinstance(child, self.cls.NiNode):
            child._flattenTree(self)

def _flattenTree(self, parent):
    """Helper function for flattenTree()."""

    # just in case
    if self == parent: raise ValueError('problem while flattening tree (cycles?)')

    # flatten NiNode grandchildren
    for child in self.children:
        if isinstance(child, self.cls.NiNode):
            child._flattenTree(parent)

    # reparent children
    for child in self.children:
        child.setTransform(child.getTransform(parent))
        parent.addChild(child)

    # remove children from self
    self.numChildren = 0
    self.children.updateSize()
